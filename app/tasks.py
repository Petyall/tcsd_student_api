import subprocess

from app.logger import logger


def get_logs():
    try:
        result = subprocess.run(["get_logs.bat"], capture_output=True, text=True, check=True)
        logger.info(f"Логи успешно обработаны: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка выполнения BAT-файла: {e}")
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка: {e}")
