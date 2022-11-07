#!/bin/bash

#Проверка внешнего IP-адреса и отправка его по электронной почте
#ДЛЯ ПРАВИЛЬНОЙ РАБОТЫ НЕОБХОДИМЫ:
#1.dns-utils
#2.msmtp


#Пути к файлам лога и конфигурации
LOG_FILE=/var/log/ip_update.log
IP_FILE=/tmp/ip_update.tmp
ERROR_FILE=/tmp/ip_update_errors.tmp
NOW=$(date)

#Перенаправление STDERROR
exec 2>$ERROR_FILE

#Функция записи ошибок в лог файл
function write_log() {
    echo $* >> $LOG_FILE
    exit 0
}

#Функция получения внешнего IP адреса
function get_external_ip() {    
    echo $(dig @resolver4.opendns.com myip.opendns.com +short -4 || write_log $NOW "Ошибка получения внешнего IP")
}

#Проверка наличия лог файла
if ! [ -f "$LOG_FILE" ] 
then
    touch $LOG_FILE
fi

#Проверка на наличие файла с предидущим IP
if ! [ -f "$IP_FILE" ] 
then
    touch $IP_FILE
    get_external_ip > $IP_FILE
    cat $IP_FILE | msmtp -a default dsk13@inbox.ru || write_log $NOW "Ошибка отправки e-mail"
else
    last_ip=$(cat $IP_FILE)
    current_ip=$(get_external_ip) 
    if ! [ $last_ip == "$current_ip" ]
    then
        get_external_ip > $IP_FILE  
        cat $IP_FILE | msmtp -a default dsk13@inbox.ru || write_log $NOW "Ошибка отправки e-mail"
    fi
fi
rm $ERROR_FILE

