import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import os
import django
import json
from datetime import datetime
from django.test import Client


def log_crm_heartbeat():
    """Log a heartbeat message every 5 minutes to confirm CRM is alive."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message + "\n")

    # Optional: Verify GraphQL hello field
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("{ hello }")
        result = client.execute(query)

        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} GraphQL responded: {result}\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} GraphQL check failed: {e}\n")

# Ensure Django is set up when cron runs standalone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
django.setup()

def update_low_stock():
    client = Client()
    mutation = """
    mutation {
        updateLowStockProducts {
            updatedProducts {
                id
                name
                stock
            }
            message
        }
    }
    """
    response = client.post("/graphql/", data={"query": mutation}, content_type="application/json")
    result = json.loads(response.content)

    log_file = "/tmp/low_stock_updates_log.txt"
    with open(log_file, "a") as f:
        f.write(f"\n[{datetime.now()}] {json.dumps(result)}\n")
