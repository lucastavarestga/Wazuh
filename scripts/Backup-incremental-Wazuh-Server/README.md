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

## 3. Baixando Script

Acesse o diretório de scripts e baixe:

```bash
cd /root/scripts
wget https://raw.githubusercontent.com/lucastavarestga/Wazuh/refs/heads/main/scripts/Backup-incremental-Wazuh-Server/backup_wazuhserver.sh
```

## 4. Edite o script para fazer as modificações necessárias de local do salvamento, o que será feito backup, e tempo de retenção, para isso utilize o nano ou vim

```bash
nano /root/scripts/backup_wazuhserver.sh
```

## 5. Permissões e Primeiro Teste

Após customizações, vamos para a parte de ajuste de permissões e realização do primeiro teste manual para validar a gravação dos dados:

```bash
chmod +x /root/scripts/backup_wazuhserver.sh
bash -x /root/scripts/backup_wazuhserver.sh
```

## 6. Validação dos Dados

Procedemos com a verificação dos arquivos gravados e do tamanho total ocupado no storage:

```bash
ls -lha /backup/bkp-server/
du -shc /backup/bkp-server/*
```

## 7. Agendamento (Crontab)

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
| ---- | ---- |
| **Autor**   | Lucas Tavares Soares |
| **Email**   | lucas@fkmais.com.br |
| **Data**    | 15/02/2026 |
| **Versão**  | 2.4 |

### Qualquer dúvida, entre em contato.

<a href="mailto:lucastavarestga@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
<a href="https://www.linkedin.com/in/lucastavarestga" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
<a href="https://youtube.com/@lucastavaressoares" target="_blank"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" target="_blank"></a>

Youtube MasterMindTI

<a href="https://www.youtube.com/@mastermindti" target="_blank"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" target="_blank"></a>
