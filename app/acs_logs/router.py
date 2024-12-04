import subprocess, os, glob, datetime

from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app.logger import logger
from app.acs_logs.schemas import LogsRequest
from app.acs_logs.utils import date_validation
from app.acs_logs.dependencies import token_manager


router = APIRouter(
    prefix="/acs_logs",
    tags=["Работа с логами СКУДа"],
)


@router.post("/", summary="Получение логов СКУДа")
def get_acs_logs(request_data: LogsRequest):
    token_is_valid: bool = Depends(token_manager.verify_token(request_data.token))

    if request_data.date == "now":
        return fetch_logs_for_current_time()
    else:
        return fetch_logs_by_date(request_data.date)


def find_latest_log_file(datetime_str: str) -> tuple[str, list] | None:
    """
    Поиск и возврат последнего лог-файла для заданной даты и времени
    
    Параметры:
    - datetime_str (str): строка с датой и временем в формате "YYYYMMDD_HHMM", используется для фильтрации файлов по дате

    Возвращаемое значение:
    - tuple[str, list] | None: кортеж, содержащий:
        - строку с максимальной меткой времени в формате "YYYYMMDD_HHMM" (например, "20241201_1530"),
        - список путей к файлам, соответствующим данной метке времени, или None, если нет подходящих файлов.
    """

    # Получение всех лог-файлов за текущий день
    log_files = glob.glob(f"{datetime_str[:8]}*.txt")

    if log_files:
        # Отсекаются все лог-файлы, не имеющие вид YYYYMMDD_HHMM.txt
        valid_files = [f for f in log_files if len(os.path.basename(f)) == 17]

        file_dates = []

        for file in valid_files:
            try:
                # Получение дат из лог-файлов
                file_timestamp = int(file[:13].replace("_", ""))
                file_dates.append(file_timestamp)
            except ValueError as e:
                logger.error(f"Ошибка при обработке файла - {e}")
                return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при обработке файлов")
        
        if file_dates:
            # Получение самого нового лог-файла из имеющихся
            latest_file_date = max(file_dates)
            return latest_file_date, valid_files
        else:
            return None


def fetch_logs_for_current_time():
    """
    Получение лог-файла для текущего времени

    Возвращаемое значение:
    - FileResponse: возврат лог-файла в формате "text/plain"
    """

    # Получение даты в момент запроса
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y%m%d_%H%M")

    # Получение самого нового лог-файла из имеющихся
    latest_log = find_latest_log_file(formatted_time)
    if latest_log:
        latest_file_date, valid_log_files = latest_log

        # Проверка для создания нового лог-файла, если самый последний существует более 2 часов
        if int(formatted_time.replace("_", "")) - latest_file_date < 120:
            # Отправка последнего лог-файла, поскольку он еще является новым
            return FileResponse(
                path=f"{str(latest_file_date)[:8]}_{str(latest_file_date)[8:]}.txt",
                filename=f"{str(latest_file_date)[:8]}_{str(latest_file_date)[8:]}.txt",
                media_type="text/plain"
            )
        else:
            # Создание нового лог-файла, поскольку последний лог-файл уже устарел
            subprocess.run(["get_logs_now.bat"])
            for file in valid_log_files:
                os.remove(file)
            return FileResponse(path=f"{formatted_time}.txt", filename=f"{formatted_time}.txt", media_type="text/plain")
    else:
        # Создание лог-файла, если на день запроса еще не существует нужного лог-файла
        subprocess.run(["get_logs_now.bat"])
        return FileResponse(path=f"{formatted_time}.txt", filename=f"{formatted_time}.txt", media_type="text/plain")
    

def fetch_logs_by_date(date: str):
    """
    Получаение лог-файла по заданной дате
    
    Параметры:
    - date (str): Строка, представляющая дату в формате "YYYYMMDD".

    Возвращаемое значение:
    - FileResponse: возврат лог-файла в формате "text/plain"
    - HTTPException: возврат ошибки, исли дата некорректна или файл не найден
    """

    validated_date = date_validation(date)
    if validated_date:
        if os.path.exists(f"{date}.txt"):
            return FileResponse(path=f"{date}.txt", filename=f"{date}.txt", media_type="text/plain")
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Файл не найден")  
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неподдерживаемый формат даты. Пример правильного формата - 20241204 (YYYYMMDD)")
