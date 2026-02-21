#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# Elaborado por Lucas Tavares Soares (Equipe FK+)
# Versao 2.5 - 21/02/2026
# Compatibilidade: Debian, Ubuntu, RHEL, CentOS, AlmaLinux, Rocky, Amazon Linux
# ------------------------------------------------------------------------------

# Identificação dinâmica de binários para portabilidade
RSYNC=$(command -v rsync)
FIND=$(command -v find)
MKDIR=$(command -v mkdir)
RM=$(command -v rm)
TEE=$(command -v tee)
DATE_CMD=$(command -v date)

# - CONFIGURACAO ---------------------------------------------------------------
HOST_NAME=$(hostname)
BACKUP_ROOT="/backup/bkp-server"
BACKUP_DIR="${BACKUP_ROOT}/${HOST_NAME}"
DATE_BKP=$(${DATE_CMD} +%Y%m%d-%H%M)
CURRENT_BACKUP_PATH="${BACKUP_DIR}/${DATE_BKP}"

# - ORIGENS E DESTINOS ---------------------------------------------------------
# 1. Sistema Operacional
DIRS_SO="/etc /root /opt"
DEST_SO="${CURRENT_BACKUP_PATH}/SistemaOperacional"

# 2. Estrutura Wazuh (Indexer, Manager, Dashboard)
DIRS_WZ="/var/ossec/etc /var/ossec/api /var/ossec/ruleset /var/ossec/bin /etc/wazuh-indexer /etc/wazuh-dashboard"
DEST_WZ="${CURRENT_BACKUP_PATH}/ConfigsWazuhServer"

# - LOGS E RETENCAO ------------------------------------------------------------
LOG_FILE="${BACKUP_DIR}/backup_rsync.log"
RETENCAO="+30"
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
   [ -f "${BACKUP_DIR}/last" ] && LAST_BKP_BASE=$(cat "${BACKUP_DIR}/last")
      
   if [ -n "${LAST_BKP_BASE}" ] && [ -d "${LAST_BKP_BASE}/${CATEGORIA}" ]; then
       LINK_PARAM="--link-dest=${LAST_BKP_BASE}/${CATEGORIA}/"
   fi

   _LOG "Sincronizando ${CATEGORIA}..."
   ${RSYNC} ${RSYNC_OPT} ${LINK_PARAM} ${ORIGEM} "${DESTINO}/" >> "${LOG_FILE}" 2>&1
}

_BACKUP () {
   _LOG "---------------------------------------------------------------------"
   _LOG "Iniciando backup de ${HOST_NAME}: $(${DATE_CMD} '+%d/%m/%Y %H:%M:%S')"

   _SYNC "${DIRS_SO}" "${DEST_SO}" "SistemaOperacional"
   _SYNC "${DIRS_WZ}" "${DEST_WZ}" "ConfigsWazuhServer"

   echo "${CURRENT_BACKUP_PATH}" > "${BACKUP_DIR}/last"

   _LOG "Limpando backups com mais de ${RETENCAO} dias..."
   ${FIND} "${BACKUP_DIR}" -maxdepth 1 -type d -mtime ${RETENCAO} -name "20*" -exec ${RM} -rf {} + >> "${LOG_FILE}" 2>&1

   _LOG "Finalizado em: $(${DATE_CMD} '+%d/%m/%Y %H:%M:%S')"
   _LOG "---------------------------------------------------------------------"
}

_BACKUP
