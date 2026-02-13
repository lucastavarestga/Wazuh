#!/usr/bin/env python3

"""
Autor: Lucas Tavares Soares
Email: lucas@fkmais.com.br
Versão: 1.7 (Produção Consolidada)
Descrição: SOC FK+ Tecnologia - Integração Telegram com melhorias.
"""

import sys
import json
import requests

# --- Configurações de Destino ---
CHAT_ID = "XXXXX" # Mantenha o ID que funcionou no teste

# Mapeamento para Personalização (Regra -> Título e Emoji)
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

def escape_markdown(text):
    """ Escapa caracteres especiais para evitar erro 400 no Telegram """
    if not text:
        return "N/A"
    return str(text).replace('_', '\\_').replace('*', '\\*').replace('`', "'")

# --- Lógica de Argumentos ---
if len(sys.argv) < 2:
    sys.exit(1)

alert_file_path = sys.argv[1]

try:
    hook_url = sys.argv[3]
except IndexError:
    sys.exit(1)

# Leitura do Alerta
with open(alert_file_path, 'r') as f:
    alert_json = json.loads(f.read())

# --- Extração e Sanitização ---
rule_id = alert_json.get('rule', {}).get('id', 'N/A')
rule_desc = escape_markdown(alert_json.get('rule', {}).get('description', 'N/A'))
rule_level = alert_json.get('rule', {}).get('level', 'N/A')
timestamp = alert_json.get('timestamp', 'N/A')
full_log = alert_json.get('full_log', 'N/A')

agent = alert_json.get('agent', {})
agent_id = agent.get('id', 'N/A')
agent_name = escape_markdown(agent.get('name', 'N/A'))
agent_ip = agent.get('ip', 'N/A')

data = alert_json.get('data', {})
win_data = data.get('win', {})
event_data = win_data.get('eventdata', {})
system_data = win_data.get('system', {})

event_id = str(system_data.get('eventID') or 'N/A')
subject_user = escape_markdown(event_data.get('subjectUserName') or data.get('srcuser') or 'N/A')
subject_domain = escape_markdown(event_data.get('subjectDomainName') or 'N/A')
target_user = escape_markdown(event_data.get('targetUserName') or data.get('dstuser') or 'N/A')
member_name = escape_markdown(event_data.get('memberName', 'N/A'))
src_ip = data.get('srcip') or event_data.get('ipAddress') or 'N/A'
system_msg = system_data.get('message', 'N/A')
computer_host = escape_markdown(system_data.get('computer') or agent_name)

# Título Dinâmico
custom_title, emoji = CUSTOM_MAP.get(rule_id, (None, None))
if custom_title:
    header = f"{emoji} *{custom_title}*"
elif str(rule_level).isdigit() and int(rule_level) >= 12:
    header = "🔥 *ALERTA CRÍTICO - SOC*"
    emoji = "⚠"
else:
    header = "🔔 *Alerta - SOC*"
    emoji = "🔍"

# Atividade AD
if event_id in ['4732', '4733', '4728', '4729', '4756', '4757']:
    detalhes_atividade = f"• *Grupo Afetado:* {target_user}\n• *Membro Alterado:* {member_name}"
else:
    detalhes_atividade = f"• *Usuário Alvo:* {target_user}"

log_clean = str(system_msg if system_msg != 'N/A' else full_log).replace('`', "'")[:250]

# --- Construção da Mensagem ---
message = (
    f"{header}\n"
    f"━━━━━━━━━━━━━━━━━━\n"
    f"📝 *Descrição:* {rule_desc}\n"
    f"📊 *ID Regra:* {rule_id} (Nível {rule_level})\n"
    f"⏰ *Data/Hora:* {timestamp}\n\n"
    f"🖥 *Origem (Agente):*\n"
    f"• *ID:* {agent_id} | *Nome:* {agent_name}\n"
    f"• *IP Agente:* {agent_ip}\n"
    f"• *Host:* {computer_host}\n\n"
    f"{emoji} *Detalhes Técnicos:*\n"
    f"• *EventID:* {event_id}\n"
    f"• *Autor da Ação:* {subject_user} ({subject_domain})\n"
    f"• *IP Origem:* {src_ip}\n"
    f"{detalhes_atividade}\n\n"
    f"📖 *Log/Mensagem:*\n"
    f"```\n{log_clean}...\n```\n"
    f"━━━━━━━━━━━━━━━━━━"
)

msg_payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
headers = {'content-type': 'application/json'}

try:
    response = requests.post(hook_url, json=msg_payload, headers=headers, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"Erro no envio: {e}")

sys.exit(0)
