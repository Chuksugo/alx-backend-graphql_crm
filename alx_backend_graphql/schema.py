import graphene
from crm.schema import CRMQuery   # <-- import CRMQuery from crm app schema

class Query(CRMQuery, graphene.ObjectType):
    pass   # No need to add fields here unless required

schema = graphene.Schema(query=Query)
