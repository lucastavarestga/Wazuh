# Backup Rsync Incremental - Wazuh Server

Este script realiza o backup incremental e modular do Wazuh Server e do Sistema Operacional de forma compativel a distribuições Linux suportadas oficialmente pelo Wazuh Server. A solução utiliza hardlinks para otimização de storage e garante a segregação total entre arquivos do SO e configurações do Wazuh, com gerenciamento automático de retenção, além de gerenciar automaticamente a retenção dos dados (padrão 30 dias).

## 1. Pré-requisitos
O script depende de ferramentas padrão presentes nos repositórios oficiais das distros suportadas (Debian, Ubuntu, RHEL, CentOS, AlmaLinux, Rocky e Amazon Linux).

# Para distribuições baseadas em Debian/Ubuntu:

```bash
apt update && apt install -y rsync wget nano findutils coreutils hostname cron tree
```

# Para distribuições baseadas em RHEL/CentOS/AlmaLinux/Rocky/Amazon Linux:

```bash
dnf install -y rsync wget nano findutils coreutils hostname cronie tree
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
/usr/bin/env bash -x /root/scripts/backup_wazuhserver.sh
```

## 6. Validação dos Dados

Procedemos com a verificação dos arquivos gravados e do tamanho total ocupado no storage:

# Visualizar a estrutura de pastas criada (Níveis de diretório)
```bash
tree -L 4 /backup/bkp-server/
```

# Verificar tamanho total e eficiência do storage
```bash
du -shc /backup/bkp-server/*
```

# Listando arquivos gravados
```bash
ls -lha /backup/bkp-server/
```

## 7. Agendamento (Crontab)

Configuramos a execução automática via cron (execução às 01:00 e 12:20):

```bash
crontab -e
```
Adicione as linhas abaixo:
Configuramos a execução automática (01:00 e 12:20):

```bash
# Backup diário do Wazuh Server e SO
00 01 * * * /usr/bin/env bash /root/scripts/backup_wazuhserver.sh >> /var/log/backup_wazuh.log 2>&1
20 12 * * * /usr/bin/env bash /root/scripts/backup_wazuhserver.sh >> /var/log/backup_wazuh.log 2>&1
```

---

## Diferenciais desta Implementação

* **Economia de Espaço**: Utiliza hardlinks via Rsync para evitar redundância de arquivos inalterados, otimizando o storage.
* **Segregação**: Organiza de forma modular as pastas do Sistema Operacional e as configurações da Wazuh (Manager, Indexer, Dashboard).
* **Retenção Automática**: Gestão nativa do ciclo de vida dos dados com expurgo automático de backups superiores a 30 dias.
* **Auditoria**: Geração de logs detalhados para acompanhamento de status e integridade de cada execução.
* **Arquitetura Agnóstica**: Compatibilidade total com a matriz oficial de SOs do Wazuh (Debian, Ubuntu, RHEL, AlmaLinux, Rocky e Amazon Linux).
* **Visibilidade Estrutural**: Uso do utilitário tree para conferência rápida e visual da hierarquia de diretórios e integridade dos dados.

---

## Informações de Versionamento

|Campo |Detalhes |
| ---- | ---- |
| **Autor**   | Lucas Tavares Soares |
| **Email**   | lucas@fkmais.com.br |
| **Data**    | 21/02/2026 |
| **Versão**  | 2.5 |

### Qualquer dúvida, entre em contato.

<a href="mailto:lucastavarestga@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
<a href="https://www.linkedin.com/in/lucastavarestga" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
<a href="https://youtube.com/@lucastavaressoares" target="_blank"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" target="_blank"></a>

Youtube MasterMindTI

<a href="https://www.youtube.com/@mastermindti" target="_blank"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" target="_blank"></a>
