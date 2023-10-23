import time
import psutil
import httpx
from prometheus_client import start_http_server, Gauge


threshold = 100

memory_usage_metric = Gauge('memory_usage_percent', 'Memory usage percentage')


def check_memory():
    memory_usage = psutil.virtual_memory().percent
    memory_usage_metric.set(memory_usage)
    if memory_usage > threshold:
        send_alert(memory_usage)


def send_alert(memory_usage):
    url = "http://flask_app:8080/alert"
    payload = {"message": f"Memory usage is {memory_usage}%"}
    httpx.post(url, json=payload)


if __name__ == "__main__":
    start_http_server(8000)
    while True:
        check_memory()
        time.sleep(60)
