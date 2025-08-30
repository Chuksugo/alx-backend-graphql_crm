import datetime
import requests

def log_crm_heartbeat():
    """Log a heartbeat message every 5 minutes to confirm CRM is alive."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message + "\n")

    # Optional: Check GraphQL hello field to verify endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            with open("/tmp/crm_heartbeat_log.txt", "a") as f:
                f.write(f"{timestamp} GraphQL endpoint responded: {response.json()}\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} GraphQL check failed: {e}\n")
