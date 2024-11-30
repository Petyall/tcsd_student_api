Временная заглушка bat-файла

@echo off
:: Получаем текущую дату и время
for /F "tokens=1-4 delims=/-. " %%i in ('date /T') do (
    set d=%%k%%j%%i
)
for /F "tokens=1-2 delims=/:" %%a in ('time /T') do (
    set t=%%a%%b
)

:: Формируем имя файла
set FileName=%d%_%t%.txt

:: Записываем текущие дату и время в файл
echo Current date: %d% >> %FileName%
echo Current time: %t% >> %FileName%

:: Сообщение об успехе
echo Файл %FileName% успешно создан!