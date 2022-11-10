REM Удаление файлов созданых позже n дней
ForFiles /p filepath /s /d -n /c "cmd /c del @FILE"
