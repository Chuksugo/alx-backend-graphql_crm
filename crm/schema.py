import re
import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

# ====================
# GraphQL Types
# ====================
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "total_amount", "order_date")


# ====================
# Input Types
# ====================
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


# ====================
# Mutations
# ====================

# ---- Create Customer ----
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        # Unique email check
        if Customer.objects.filter(email=input.email).exists():
            raise Exception("Email already exists")

        # Phone validation if provided
        if input.phone:
            if not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', input.phone):
                raise Exception("Invalid phone format. Use +1234567890 or 123-456-7890")

        customer = Customer(name=input.name, email=input.email, phone=input.phone)
        customer.full_clean()
        customer.save()

        return CreateCustomer(customer=customer, message="Customer created successfully")


# ---- Bulk Create Customers ----
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @transaction.atomic
    def mutate(self, info, input):
        created = []
        errors = []

        for idx, cust in enumerate(input, start=1):
            try:
                if Customer.objects.filter(email=cust.email).exists():
                    raise ValidationError(f"Email '{cust.email}' already exists")

                if cust.phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', cust.phone):
                    raise ValidationError(f"Invalid phone format for {cust.email}")

                obj = Customer(name=cust.name, email=cust.email, phone=cust.phone)
                obj.full_clean()
                obj.save()
                created.append(obj)

            except Exception as e:
                errors.append(f"Row {idx}: {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)


# ---- Create Product ----
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(default_value=0)

    product = graphene.Field(ProductType)
    message = graphene.String()

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product, message="Product created successfully")


# ---- Create Order ----
class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime(required=False)

    order = graphene.Field(OrderType)
    message = graphene.String()

    def mutate(self, info, customer_id, product_ids, order_date=None):
        # Validate customer
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        # Validate product list
        if not product_ids:
            raise Exception("At least one product must be selected")

        products = Product.objects.filter(id__in=product_ids)
        if len(products) != len(product_ids):
            raise Exception("One or more product IDs are invalid")

        # Create order
        order = Order.objects.create(
            customer=customer,
            order_date=order_date or timezone.now()
        )
        order.products.set(products)
        order.calculate_total()  # assumes you implemented calculate_total in model
        order.save()

        return CreateOrder(order=order, message="Order created successfully")


# ====================
# CRM Query + Mutation
# ====================
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
