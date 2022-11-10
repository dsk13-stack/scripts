REM Простой сканер IP адресов подсети с записью результатов в файл
chcp 65001
echo off
for /L %i in (1, 1, 255) do if %i EQU 255 (echo Scan finished) else (ping /n 1 /w 100 192.168.1.%i) | findstr "TTL" >> C:\ScanResult.txt
pause
