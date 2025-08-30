#!/usr/bin/env python3
"""
send_order_reminders.py
Query pending orders within the last 7 days via GraphQL and log reminders.
"""

import sys
import asyncio
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# Define query (adjust field names if different in your schema)
query = gql("""
    query RecentOrders($since: DateTime!) {
        orders(orderDate_Gte: $since) {
            id
            customer {
                email
            }
        }
    }
""")

async def main():
    # Calculate 7 days ago
    since_date = (datetime.utcnow() - timedelta(days=7)).isoformat()

    # Setup GraphQL transport
    transport = RequestsHTTPTransport(
        url=GRAPHQL_ENDPOINT,
        verify=False,
        retries=3,
    )

    # Setup client
    client = Client(transport=transport, fetch_schema_from_transport=False)

    try:
        result = await client.execute_async(query, variable_values={"since": since_date})
        orders = result.get("orders", [])

        with open("/tmp/order_reminders_log.txt", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for order in orders:
                order_id = order.get("id")
                email = order.get("customer", {}).get("email")
                f.write(f"{timestamp} - Reminder for Order {order_id}, Customer Email: {email}\n")

        print("Order reminders processed!")

    except Exception as e:
        print(f"Error querying orders: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
