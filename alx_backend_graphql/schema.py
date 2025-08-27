import graphene
from crm.schema import CRMQuery   

class Query(CRMQuery, graphene.ObjectType):
    pass   # No need to add fields here unless required

schema = graphene.Schema(query=Query)
