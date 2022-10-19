# Проверка URL bash
#!/bin/bash
echo "Enter URL"
read url

match=$(echo $url | awk '/^((http:\/\/|https:\/\/|ftp:\/\/)|www.)+(([a0-z9\-])+\.){1,3}([a0-z9]{2,3}(\:|\/|)){1}(\S*(\:|\/|))*/{print $1}')

if [ "$url" = "$match" ]; 
then 
	echo "URL OK"
else
	echo "Invalid URL"
fi

# Проверка URL Python
#!/usr/bin/env python3
import re

print("Enter URL")
url = input()

regex = r"^((http:\/\/|https:\/\/|ftp:\/\/)|www.)+(([a0-z9\-])+\.){1,3}([a0-z9]{2,3}(\:|\/|)){1}(\S*(\:|\/|))*"
match = re.search(regex,url)

if match and match.group(0) == url:
    print("URL OK")
else:
    print("Invalid URL")

# Обработка всех трех стандартных потоков Python
#!/usr/bin/env python3
import sys

sys.stdout.write("Hello, input to integers to divide through a space" + "\n")
inp = [int(line) for line in sys.stdin.read().strip().split()]
sys.stdout.write("" + "\n")

try:
    sys.stdout.write("Result: " + str(inp[0] / inp[1]) + "\n")
except Exception as error:
    sys.stderr.write("Error: " + str(error) + "\n")
    
    
    
#Проверка внешнего IP-адреса и отправка его по электронной почте    
#Пути к файлам лога и конфигурации
LOG_FILE=/var/log/ip_updater.log
IP_FILE=/var/tmp/ip_updater
ERROR_FILE=/var/tmp/errors.tmp
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
    cat $IP_FILE | mutt -s "Новый IP адрес" -- dsk13@inbox.ru || write_log $NOW "Ошибка отправки e-mail"
else
    last_ip=$(cat $IP_FILE)
    current_ip=$(get_external_ip) 
    if ! [ $last_ip == "$current_ip" ]
    then
        get_external_ip > $IP_FILE  
        cat $IP_FILE | mutt -s "Новый IP адрес" -- dsk13@inbox.ru || write_log $NOW "Ошибка отправки e-mail"
    fi
fi
rm $ERROR_FILE
