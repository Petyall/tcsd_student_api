import subprocess, os, glob, datetime

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.acs_logs.schemas import LogsRequest
from app.acs_logs.utils import date_validation
from app.acs_logs.authorization import verify_token


router = APIRouter(
    prefix="/acs_logs",
    tags=["Работа с логами СКУДа"],
)


@router.post("/")
def get_acs_logs(data: LogsRequest):
    token: bool = Depends(verify_token(data.token))

    if data.date == "now":
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M")

        files_with_current_date = glob.glob(f"{formatted_datetime[:8]}*.txt")

        if files_with_current_date:
            files = []
            for file in files_with_current_date:
                file_date = int(file[:13].replace("_", ""))
                files.append(file_date)
            file_date = max(files)
            if int(formatted_datetime.replace("_", "")) - file_date < 120:
                return FileResponse(
                    path=f"{str(file_date)[:8]}_{str(file_date)[8:]}.txt",
                    filename=f"{str(file_date)[:8]}_{str(file_date)[8:]}.txt",
                    media_type="text/plain"
                )
            else:
                init_file = subprocess.run(["get_logs_now.bat"])
                for file in files_with_current_date:
                    os.remove(file)
                return FileResponse(
                    path=f"{formatted_datetime}.txt",
                    filename=f"{formatted_datetime}.txt",
                    media_type="text/plain"
                )
        else:
            init_file = subprocess.run(["get_logs_now.bat"])
            return FileResponse(
                path=f"{formatted_datetime}.txt",
                filename=f"{formatted_datetime}.txt",
                media_type="text/plain"
            )

        
    else:
        date = date_validation(data.date)
        if date:
            if os.path.exists(f"{data.date}.txt"):
                return FileResponse(
                    path=f"{data.date}.txt",
                    filename=f"{data.date}.txt",
                    media_type="text/plain"
                )
            else:
                return "file not found"  
        else:
            return "unsupported date format"
