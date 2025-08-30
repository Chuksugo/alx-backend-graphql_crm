# crm/tasks.py
from celery import shared_task
from datetime import datetime
import requests

@shared_task
def generate_crm_report():
    """
    Generate a CRM report and log details into /tmp/crm_report_log.txt
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Example external API call (you can adjust/remove this)
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
        data = response.json()
    except Exception as e:
        data = {"error": str(e)}

    log_entry = f"[{timestamp}] CRM Report Generated: {data}\n"

    with open("/tmp/crm_report_log.txt", "a") as log_file:
        log_file.write(log_entry)

    return log_entry
