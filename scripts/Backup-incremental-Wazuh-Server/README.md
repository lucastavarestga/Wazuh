# Backup Rsync Incremental - Wazuh Server

Este script realiza o backup incremental e modular do Wazuh Server e do Sistema Operacional, utilizando hardlinks para otimizar o espaço em disco, garantindo a segregação total entre configurações e arquivos do sistema, além de gerenciar automaticamente a retenção dos dados (padrão 30 dias).

## 1. Pré-requisitos (Debian/Ubuntu)
Certifique-se de que os pacotes necessários estão instalados no seu Wazuh Manager:

```bash
apt update && apt install -y rsync findutils coreutils bash
```

## 2. Preparação do Ambiente

Procedemos com a criação do diretório para os scripts e para o armazenamento dos backups:

```bash
mkdir -p /root/scripts /backup
```

## 3. Instalação do Script

Crie o arquivo do script e insira o conteúdo técnico:

```bash
nano /root/scripts/backup_wazuhserver.sh
```

### Conteúdo do Script

```bash
#!/usr/bin/env bash  
  
# ----------------------------------  
# Elaborado por Lucas Tavares Soares  
# (Equipe FK+)  
# Versao 2.4 - 15/02/2026  
# - Estrutura Simplificada e Modular  
# ----------------------------------  
  
RSYNC=`which rsync`  
FIND=`which find`  
MKDIR=`which mkdir`  
RM=`which rm`  
TEE=`which tee`  
DATE_CMD=`which date`  
  
# - CONFIGURACAO ---------------------------------------------------------------  
HOST_NAME='WAZUH-SERVER'  
BACKUP_ROOT="/backup/bkp-server"  
BACKUP_DIR="${BACKUP_ROOT}/${HOST_NAME}"  
DATE_BKP=`${DATE_CMD} +%Y%m%d-%H%M`  
CURRENT_BACKUP_PATH="${BACKUP_DIR}/${DATE_BKP}"  
  
# - ORIGENS E DESTINOS ---------------------------------------------------------  
# 1. Sistema Operacional  
DIRS_SO="/etc /root /opt"  
DEST_SO="${CURRENT_BACKUP_PATH}/SistemaOperacional"  
  
# 2. Configuracoes Wazuh Server  
DIRS_WZ="/var/ossec/etc /var/ossec/api /var/ossec/ruleset /var/ossec/bin"  
DEST_WZ="${CURRENT_BACKUP_PATH}/ConfigsWazuhServer"  
  
# - LOGS E RETENCAO ------------------------------------------------------------  
LOG_FILE="${BACKUP_DIR}/backup_rsync.log"  
RETENCAO="+30"  
# Excluimos logs e excessos de forma global para o rsync  
RSYNC_OPT="-av --delete --stats --exclude=/var/ossec/logs/* --exclude=/var/log/* --exclude=/tmp/*"  
  
# - PREPARACAO -----------------------------------------------------------------  
[ ! -d "${BACKUP_DIR}" ] && ${MKDIR} -p "${BACKUP_DIR}"  
  
_LOG() {  
   echo "$1" | ${TEE} -a "${LOG_FILE}"  
}  
  
# - EXECUCAO RSYNC COM HARDLINKS -----------------------------------------------  
_SYNC() {  
   local ORIGEM=$1  
   local DESTINO=$2  
   local CATEGORIA=$3  
   local LAST_BKP_BASE=""  
   local LINK_PARAM=""  
  
   [ ! -d "${DESTINO}" ] && ${MKDIR} -p "${DESTINO}"  
  
   # Recupera o caminho do ultimo backup para esta categoria especifica  
   [ -f "${BACKUP_DIR}/last" ] && LAST_BKP_BASE=$(cat "${BACKUP_DIR}/last")  
      
   # Se existir backup anterior, aponta o link-dest para a subpasta correta  
   if [ -n "${LAST_BKP_BASE}" ] && [ -d "${LAST_BKP_BASE}/${CATEGORIA}" ]; then  
       LINK_PARAM="--link-dest=${LAST_BKP_BASE}/${CATEGORIA}/"  
   fi  
  
   _LOG "Sincronizando ${CATEGORIA}..."  
   ${RSYNC} ${RSYNC_OPT} ${LINK_PARAM} ${ORIGEM} "${DESTINO}/" >> "${LOG_FILE}" 2>&1  
}  
  
_BACKUP () {  
   _LOG "---------------------------------------------------------------------"  
   _LOG "Iniciando backup de ${HOST_NAME}: `${DATE_CMD} '+%d/%m/%Y %H:%M:%S'`"  
  
   # Executa a sincronizacao por grupos  
   _SYNC "${DIRS_SO}" "${DEST_SO}" "SistemaOperacional"  
   _SYNC "${DIRS_WZ}" "${DEST_WZ}" "ConfigsWazuhServer"  
  
   # Atualiza o ponteiro 'last' com a raiz do backup de hoje  
   echo "${CURRENT_BACKUP_PATH}" > "${BACKUP_DIR}/last"  
  
   # Limpeza  
   _LOG "Limpando backups com mais de ${RETENCAO} dias..."  
   ${FIND} "${BACKUP_DIR}" -maxdepth 1 -type d -mtime ${RETENCAO} -name "20*" -exec ${RM} -rf {} + >> "${LOG_FILE}" 2>&1  
  
   _LOG "Finalizado em: `${DATE_CMD} '+%d/%m/%Y %H:%M:%S'`"  
   _LOG "---------------------------------------------------------------------"  
}  
  
_BACKUP
```

## 4. Permissões e Primeiro Teste

Ajustamos as permissões e realizamos o primeiro teste manual para validar a gravação dos dados:

```bash
chmod +x /root/scripts/backup_wazuhserver.sh
bash -x /root/scripts/backup_wazuhserver.sh
```

## 5. Validação dos Dados

Procedemos com a verificação dos arquivos gravados e do tamanho total ocupado no storage:

```bash
ls -lha /backup/bkp-server/
du -shc /backup/bkp-server/*
```

## 6. Agendamento (Crontab)

Configuramos a execução automática via cron (execução às 01:00 e 12:20):

```bash
crontab -e
```

Adicione as linhas abaixo:

```bash
# Backup diário do Wazuh Server e SO (Padrão FK+)
00 01 * * * /bin/bash /root/scripts/backup_wazuhserver.sh >> /var/log/backup_wazuh.log 2>&1
20 12 * * * /bin/bash /root/scripts/backup_wazuhserver.sh >> /var/log/backup_wazuh.log 2>&1
```

---

## Diferenciais desta Implementação

* **Economia de Espaço**: Utiliza hardlinks para arquivos inalterados entre backups.
* **Segregação**: Pastas distintas para SO e configurações específicas do Wazuh.
* **Retenção Inteligente**: Limpeza automática de arquivos com mais de 30 dias.
* **Logging**: Acompanhamento detalhado do status de cada execução.
---

## Informações de Versionamento

| Campo | Detalhes |
| --- | --- |
| **Autor** | Lucas Tavares Soares |
| **Email** | lucas@fkmais.com.br |
| **Data** | 15/02/2026 |
| **Versão** | 2.4 |

<a href="mailto:lucastavarestga@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
<a href="https://www.google.com/search?q=https://www.linkedin.com/in/lucastavarestga" target="_blank"><img src="https://www.google.com/search?q=https://img.shields.io/badge/-LinkedIn-0077B5%3Fstyle%3Dfor-the-badge%26logo%3Dlinkedin%26logoColor%3Dwhite" target="_blank"></a>
