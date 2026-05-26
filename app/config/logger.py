import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger.json import JsonFormatter

Path("./app/logs").mkdir(exist_ok=True)

formatter = JsonFormatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

logging.basicConfig(
    level = logging.INFO,
)

def create_logger(logger_name: str, logger_file: str):
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = TimedRotatingFileHandler(
            filename=f"app/logs/{logger_file}",
            when = "midnight",
            interval=1,
            backupCount=7
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


logger = {
    "app" : create_logger("app","app.jsonl"),
    "middleware": create_logger("middleware","middleware.jsonl"),
    "POST" : create_logger("post","post.jsonl"),
    "GET" : create_logger("get","get.jsonl"),
    "PATCH": create_logger("patch_logger","patch.jsonl"),
    "DELETE": create_logger("delete_logger","delete.jsonl")
}
    

