import os
from celery import shared_task
from django.utils import timezone
from crm.models import Customer, Order

@shared_task
def generate_crm_report():
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total_amount_sum=models.Sum("totalamount"))["total_amount_sum"] or 0

    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

    log_file = "/tmp/crm_report_log.txt"
    with open(log_file, "a") as f:
        f.write(report)

    return report
