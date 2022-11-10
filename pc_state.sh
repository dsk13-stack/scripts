#!/bin/bash
#Сбор данных о состоянии системы в файл 
# Для корректной работы необходимы пакеты ls_sensors и hdd_temp (можно использовать smartctl как альтернативу)

# Путь к hddtemp указываем явно, чтобы при запуске через CRON не получить ошибку об отсутствии hddtemp  
HDD_TEMP=/usr/sbin/hddtemp
PATH_TO_FILE=$1

echo " " > $PATH_TO_FILE
exec 2>>$PATH_TO_FILE
echo "Время работы" >> $PATH_TO_FILE
echo $(uptime | sed 's/.*up \([^,]*\), .*/\1/') >> $PATH_TO_FILE
echo "Температура CPU" >> $PATH_TO_FILE
echo $(sensors | grep "CPU Temp*" | cut -d " " -f6) >> $PATH_TO_FILE
echo "Температура MB" >> $PATH_TO_FILE
echo $(sensors | grep "MB Temp*" | cut -d " " -f7) >> $PATH_TO_FILE
echo "Температура HDD" >> $PATH_TO_FILE
echo $($HDD_TEMP /dev/sda | cut -d " " -f3) >> $PATH_TO_FILE
echo "Средняя загрузка CPU" >> $PATH_TO_FILE
echo $(cat /proc/loadavg | cut -d" " -f1) >> $PATH_TO_FILE 
echo "Использовано оперативной памяти" >> $PATH_TO_FILE
echo $(free -g -h -t | grep "Память:" | cut -d " " -f15) >> $PATH_TO_FILE
echo "Всего оперативной памяти" >> $PATH_TO_FILE
echo $(free -g -h -t | grep "Память:" | cut -d " " -f8) >> $PATH_TO_FILE
echo "Свободное место на диске" >> $PATH_TO_FILE
echo $(df -h /dev/sda3 |grep /dev | cut -d " " -f20) >> $PATH_TO_FILE
