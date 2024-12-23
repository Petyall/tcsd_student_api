# TCSD student API

## Описание

Веб-приложение создано с использованием фреймворка [FastAPI](https://fastapi.tiangolo.com/). Основная цель приложения – предоставление доступа к логам системы контроля управления доступом (СКУД). Приложение позволяет пользователям запрашивать логи за определённые даты через API, а также автоматически обновляет токен авторизации и выполняет сбор логов по расписанию.

## Функциональность

### ./main.py
Основной файл приложения, который инициализирует сервер FastAPI и запускает планировщик задач APScheduler для автоматического обновления токена и сбора логов
- get_logs: функция для запуска bat-файла, обрабатывающего логи (получение логов работы за весь прошлый день по расписанию в 05:30 по МСК). Логика обработки ошибок включает вывод сообщений о неудачном выполнении bat-файла или непредвиденных исключениях
- lifespan: контекстный менеджер, включающий старт и остановку планировщика задач

### ./acs_logs/router.py
Файл маршрутизатора, содержащий маршруты для работы с логами СКУД
localhost:8000/acs_logs/: POST-маршрут для получения логов. Принимает запрос с указанием даты и токеном авторизации
- Если дата указана как "now", то возвращаются текущие логи с условием проверки, что последние логи не были взяты дольше чем 120 минут назад (для оптимизации нагрузки на сервер) 
- Если дата указана как YYYYMMDD (строго в таком формате), то проверяется наличие файла с указанной датой. Если файл не был найден, то выведется соответствующая ошибка (по какой-то причине сервер не смог сгененировать логи на заданную дату, либо же эта дата еще не наступила)

### ./acs_logs/authorization.py
Модуль, отвечающий за генерацию и проверку JWT-токенов авторизации. Токены хранятся локально в файле и имеют срок действия, определяемый настройками приложения
- generate_token: генерация нового JWT-токена с заданным сроком действия
- verify_token: проверка предоставленного пользователем JWT-токена на валидность

## Использование API
Для получения логов необходимо отправить POST-запрос на маршрут /acs_logs/ с телом запроса в формате JSON, содержащим дату и токен авторизации:
```json
{
    "date": "YYYYMMDD",
    "token": "<токен>"
}
```
или:
```json
{
    "date": "now",
    "token": "<токен>"
}
```
В ответе будет возвращён файл с логами за указанную дату, либо сообщение об ошибке, если файл не найден или формат даты неверный

## Автоматическое обновление токена и сбор логов
Планировщик задач выполняет следующие задачи:
- Обновление токена авторизации выполняется раз в месяц (в 23:59 последнего дня месяца)
- Сбор логов осуществляется ежедневно в 05:30
Эти параметры могут быть изменены в файле main.py

## Настройки безопасности
Токены авторизации генерируются с использованием алгоритма HS256 и хранятся локально в файле, указанном в конфигурации. Срок действия токена определяется настройкой TOKEN_EXPIRY_DAYS в конфигурационном модуле

## Получение логов работы СКУД
За получение логов отвечают два bat-файла get_logs.bat и get_logs_now.bat
- get_logs.bat Используется планировщиком задач для ежедневного сбора логов
- get_logs_now.bat Запрашивает логи непосредственно при обращении к API

## Установка и запуск

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/Petyall/tcsd_student_api.git .
```

### Шаг 2: Создание и активация виртуального окружения 

Для Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate или 
```

Для Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Шаг 3: Установка необходимых зависимостей 
```bash
pip3 install -r requirements.txt
```

### Шаг 4: Инициализация .env файла (пример данных изображен в файле .env_example)
```bash
touch .env
```

### Шаг 5: Запуск локального сервера 
```bash
uvicorn app.main:app
```
