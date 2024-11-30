Временная заглушка bat-файла

@echo off
:: Получаем текущую дату и время
for /F "tokens=1-4 delims=/-. " %%i in ('date /T') do (
    set d=%%k%%j%%i
)

:: Формируем имя файла
set FileName=%d%.txt

:: Записываем текущие дату и время в файл
echo Current date: %d% >> %FileName%

:: Сообщение об успехе
echo Файл %FileName% успешно создан!