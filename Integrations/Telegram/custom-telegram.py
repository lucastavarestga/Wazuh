#!/usr/bin/env python3

import sys
import json
import requests

# --- Configurações de Destino ---
CHAT_ID = "XXXXX"

# Dicionário de Mapeamento para Personalização (Regra -> Título e Emoji)
CUSTOM_MAP = {
    "60109": ("✅ USUÁRIO CRIADO OU ATIVADO", "👤"),
    "60110": ("⚙ CONTA DE USUÁRIO ALTERADA", "🔄"),
    "60111": ("🚫 USUÁRIO EXCLUÍDO OU DESATIVADO", "❌"),
    "60115": ("🔒 CONTA BLOQUEADA (Múltiplas Falhas)", "🔐"),
    "60128": ("🔑 FALHA DE LOGON: Senha Expirada", "⏳"),
    "60133": ("🔓 USUÁRIO DESBLOQUEADO", "🔓"),
    "60130": ("🔒 CONTA BLOQUEADA (Lockout)", "🛑"),
    "60204": ("⚠ MÚLTIPLAS FALHAS DE LOGON WINDOWS", "🛡"),
    "60154": ("🚨 ALTERAÇÃO EM GRUPO ADMINISTRADORES", "🔥"),
    "18219": ("🚨 ALTERAÇÃO EM DOMAIN CONTROLLERS", "🏰"),
    "18142": ("🔓 USUÁRIO DESBLOQUEADO (Global)", "✅"),
    "18138": ("🔒 CONTA BLOQUEADA (Lockout Global)", "🚫")
}

# Leitura de parâmetros do Wazuh
alert_file_path = sys.argv[1]
hook_url = sys.argv[3]

with open(alert_file_path, 'r') as f:
    alert_json = json.loads(f.read())

# --- Extração de Dados Globais ---
rule_id = alert_json.get('rule', {}).get('id', 'N/A')
rule_desc = alert_json.get('rule', {}).get('description', 'N/A')
rule_level = alert_json.get('rule', {}).get('level', 'N/A')
timestamp = alert_json.get('timestamp', 'N/A')
full_log = alert_json.get('full_log', 'N/A')

agent = alert_json.get('agent', {})
agent_id = agent.get('id', 'N/A')
agent_name = agent.get('name', 'N/A')
agent_ip = agent.get('ip', 'N/A')

# --- Extração de Dados Técnicos (Windows/Linux) ---
data = alert_json.get('data', {})
win_data = data.get('win', {})
event_data = win_data.get('eventdata', {})
system_data = win_data.get('system', {})

event_id = str(system_data.get('eventID') or 'N/A')
subject_user = event_data.get('subjectUserName') or data.get('srcuser') or 'N/A'
subject_domain = event_data.get('subjectDomainName') or 'N/A'
target_user = event_data.get('targetUserName') or data.get('dstuser') or 'N/A'
member_name = event_data.get('memberName', 'N/A')
src_ip = data.get('srcip') or event_data.get('ipAddress') or 'N/A'
system_msg = system_data.get('message', 'N/A')
computer_host = system_data.get('computer') or agent_name

# --- Lógica de Título Dinâmico ---
custom_title, emoji = CUSTOM_MAP.get(rule_id, (None, None))

if custom_title:
    header = f"{emoji} *{custom_title}*"
elif int(rule_level) >= 12:
    header = "🔥 *ALERTA CRÍTICO - SOC FK+ Tecnologia*"
    emoji = "⚠"
else:
    header = "🔔 *Alerta - SOC FK+ Tecnologia*"
    emoji = "🔍"

# --- Bloco de Atividade Especial para AD ---
if event_id in ['4732', '4733', '4728', '4729', '4756', '4757']:
    detalhes_atividade = f"• *Grupo Afetado:* {target_user}\n• *Membro Alterado:* {member_name}"
else:
    detalhes_atividade = f"• *Usuário Alvo:* {target_user}"

# --- Montagem da Mensagem Final ---
message = f"""{header}
━━━━━━━━━━━━━━━━━━
📝 *Descrição:* {rule_desc}
📊 *ID Regra:* {rule_id} (Nível {rule_level})
⏰ *Data/Hora:* {timestamp}

🖥 *Origem (Agente):*
• *ID:* {agent_id} | *Nome:* {agent_name}
• *IP Agente:* {agent_ip}
• *Host:* {computer_host}

{emoji} *Detalhes Técnicos:*
• *EventID:* {event_id}
• *Autor da Ação:* {subject_user} ({subject_domain})
• *IP Origem:* {src_ip}
{detalhes_atividade}

📖 *Log/Mensagem:*
`{str(system_msg if system_msg != 'N/A' else full_log)[:250]}...`
━━━━━━━━━━━━━━━━━━"""

# --- Envio ---
msg_payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

try:
    response = requests.post(hook_url, headers=headers, data=json.dumps(msg_payload), timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"Erro no envio: {e}")

sys.exit(0)

