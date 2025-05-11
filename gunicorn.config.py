import loguru
import os
import sys

loguru.logger.remove()
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> - <level>{message}</level>"
loguru.logger.add(sys.stderr, format=log_format, level="TRACE", colorize=True)
loguru.logger = loguru.logger.opt(colors=True)

workers = os.getenv("GUNICORN_WORKER_COUNT", 8)
threads = os.getenv("GUNICORN_THREADS", 8)
timeout = os.getenv("GUNICORN_TIMEOUT", 60)
# max_requests = 100
backlog = os.getenv("GUNICORN_BACKLOG", 16)
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:1180')

def on_starting(server):
    loguru.logger.info(f"Workers=<red>{workers}</red>, Threads=<red>{threads}</red>, Timeout=<red>{timeout}</red>, Backlog=<red>{backlog}</red>")