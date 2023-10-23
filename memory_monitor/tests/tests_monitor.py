import httpx
import psutil
from unittest.mock import MagicMock

from ..src.main import check_memory, send_alert, memory_usage_metric


def test_check_memory():
    psutil.virtual_memory = MagicMock(return_value=(50, 50, 50, 50, 50, 50))
    memory_usage_metric_set = MagicMock()
    memory_usage_metric.set = memory_usage_metric_set
    check_memory()
    psutil.virtual_memory.assert_called_once()
    memory_usage_metric_set.assert_called_once_with(50)


def test_send_alert():
    httpx.post = MagicMock()
    send_alert(101)
    httpx.post.assert_called_once_with(
        "http://flask_app:8080/alert",
        json={"message": "Memory usage is 101%"}
    )
