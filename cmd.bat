REM Удаление файлов созданых позже n дней
ForFiles /p filepath /s /d -n /c "cmd /c del @FILE"

REM Простой сканер IP адресов подсети с записью результатов в файл
chcp 65001
echo off
for /L %i in (1, 1, 255) do if %i EQU 255 (echo Scan finished) else (ping /n 1 /w 100 192.168.1.%i) | findstr "TTL" >> C:\ScanResult.txt
pause

REM Копия файлов, по изменению 
Xcopy SourcePATH DestinationPath /E /Y /D

REM Присвоение адаптеру статического IP и DHCP
netsh interface ipv4 set address name="Ethernet" static 192.168.0.250 255.255.255.0
netsh interface ipv4 set address name="Ethernet" source=dhcp

