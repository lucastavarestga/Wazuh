# Integração Wazuh + Telegram
Este repositório contém os scripts necessários para integrar o Wazuh Manager ao Telegram, permitindo o envio de alertas críticos de forma personalizada para monitoramento de infraestruturas Windows (Active Directory) e Linux.

Seguem as instruções para download e uso da integração.

## 1. Instalar Dependências
No seu Wazuh Manager (Ubuntu/Debian), garanta que o Python e as bibliotecas de requisição estejam instalados:

```bash
apt update ; apt install python3 python3-pip python3-requests nano -y
```

## 2. Baixar os Arquivos
Acesse o diretório de integrações e baixe os arquivos diretamente do GitHub:

```bash
cd /var/ossec/integrations
wget https://raw.githubusercontent.com/lucastavarestga/Wazuh/main/Integrations/Telegram/custom-telegram
wget https://raw.githubusercontent.com/lucastavarestga/Wazuh/main/Integrations/Telegram/custom-telegram.py
```

## 3. Definindo as Permissões
Ajustando as permissões para que o Wazuh possa executar o script:

```bash
chmod +x /var/ossec/integrations/custom-telegram*
chown root:wazuh /var/ossec/integrations/custom-telegram*
```

## 4. Configuração
Configurar o CHAT_ID
Edite o script Python para inserir o ID do seu chat/grupo do Telegram:

```bash
nano /var/ossec/integrations/custom-telegram.py
```
Altere a linha: CHAT_ID = "xxxx"

## 5. Configurar o ossec.conf
Adicione o bloco abaixo no arquivo /var/ossec/etc/ossec.conf para ativar a integração:

```
<integration>
   <name>custom-telegram</name>
   <hook_url>https://api.telegram.org/bot<SUA_API_AQUI>/sendMessage</hook_url>
   <level>12</level>
   <rule_id>60109, 60110, 60111, 60115, 60128, 60133, 60130, 60204, 60154, 18219, 18142, 18138</rule_id>
   <alert_format>json</alert_format>
 </integration>
```
Explicação dos campos:

name: Nome do script disparador.
hook_url: Endpoint da API do Bot do Telegram.
level: Envia todos os alertas de nível 12 ou superior.
rule_id: Força o envio de regras específicas (AD e Segurança), independente do nível.
alert_format: Define o envio dos dados em formato JSON para parsing detalhado.

## 6. Valide a sintaxe

```
/var/ossec/bin/wazuh-analysisd -t
```

## 7. Se estiver tudo certo, reinicie o wazuh-manager

```
systemctl restart wazuh-manager
```

## 8. Resumo da Versão
O script processará e enviará:
* **Alertas Críticos Windows/AD**: Criação/exclusão de usuários, alteração de grupos administradores, bloqueio de contas (lockout) e troca de senhas.
* **Alertas Linux**: Logins SSH, falhas críticas e atividades de sistema.
* **Personalização**: Títulos em Português-BR e ícones de identificação visual.

## 9. Informações de Versionamento

| Campo | Detalhes |
| :--- | :--- |
| **Nome** | Lucas Tavares Soares |
| **Email** | lucas@fkmais.com.br |
| **Data** | 13/02/2026 |
| **Versão** | 1.0.2 |

### Qualquer dúvida, entre em contato.

<a href="mailto:lucastavarestga@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
<a href="https://www.linkedin.com/in/lucastavarestga" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
<a href="https://youtube.com/@lucastavaressoares" target="_blank"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" target="_blank"></a>

Youtube MasterMindTI

<a href="https://www.youtube.com/@mastermindti" target="_blank"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" target="_blank"></a>
