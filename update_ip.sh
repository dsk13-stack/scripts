#!/bin/bash

#Проверка внешнего IP-адреса и отправка его по электронной почте
#ДЛЯ ПРАВИЛЬНОЙ РАБОТЫ НЕОБХОДИМЫ:
#1.dns-utils
#2.msmtp


LOG_FILE=/var/log/ip_update.log
IP_FILE=/tmp/ip_update.tmp
ERROR_FILE=/tmp/ip_update_errors.tmp
NOW=$(date +'%F %T')

exec 2>$ERROR_FILE

function write_log() {
    echo "$NOW: $*" >> $LOG_FILE
}

function get_external_ip() {    
    local ip=$(dig @resolver4.opendns.com myip.opendns.com +short -4)
    if [ $? -ne 0 ]; then
        write_log "Failed to retrieve external IP"
        exit 1
    fi
    echo "$ip"
}

if [ ! -f "$LOG_FILE" ]; then
    touch "$LOG_FILE"
fi

if [ ! -f "$IP_FILE" ]; then
    touch "$IP_FILE"
    get_external_ip > "$IP_FILE"
    msmtp -a default user@gmail.com < "$IP_FILE" || write_log "Failed to send email"
else
    last_ip=$(cat "$IP_FILE")
    current_ip=$(get_external_ip) 
    if [ "$last_ip" != "$current_ip" ]; then
        echo "$current_ip" > "$IP_FILE"
        msmtp -a default dsk13@inbox.ru < "$IP_FILE" || write_log "Failed to send email"
    fi
fi
rm "$ERROR_FILE"
