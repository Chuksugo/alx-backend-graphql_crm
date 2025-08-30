#!/bin/bash

# Script: clean_inactive_customers.sh
# Purpose: Delete inactive customers (no orders for over a year) and log the result.

# Navigate to project root
cd /c/Users/FLOWER/Desktop/alx-backend-graphql_crm

# Run Django shell command to delete inactive customers
deleted_count=$(python3 manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)

# Customers with no orders in the last year
inactive_customers = Customer.objects.filter(orders__isnull=True) | Customer.objects.exclude(orders__created_at__gte=one_year_ago)
inactive_customers = inactive_customers.distinct()

count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the cleanup result
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
