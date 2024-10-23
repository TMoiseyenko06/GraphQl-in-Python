import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Item as ItemModel
from sqlalchemy.orm import Session
from database import db
from sqlalchemy import select

class Item(SQLAlchemyObjectType):
    class Meta:
        model = ItemModel

class Query(graphene.ObjectType):
    items = graphene.List(Item)

    def resolve_items(self, info):
        return db.session.execute(db.select(ItemModel)).scalars()
    
class AddItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        category = graphene.String(required=True)

    item = graphene.Field(Item)

    def mutate(self, info, name, price, category):
        with Session(db.engine) as session:
            with session.begin():
                item = ItemModel(name=name,price=price,category=category)
                session.add(item)

            session.refresh(item)
            return AddItem(item=item)
    
class EditItem(graphene.Mutation):
    class Arguments:
        item_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        category = graphene.String(required=True)

    item = graphene.Field(Item)

    def mutate(self, info, item_id, name, price, category):
        with Session(db.engine) as session:
            with session.begin():
                item = session.get(ItemModel,item_id)
                item.name = name
                item.price = price
                item.category = category
                session.commit()
                
                return EditItem(item=item)
            
class DeleteItemResponse(graphene.ObjectType):
    message = graphene.String()
            
class DeleteItem(graphene.Mutation):
    class Arguments:
        item_id = graphene.Int(required=True)

    Output = DeleteItemResponse
    
    def mutate(self,info,item_id):
        with Session(db.engine) as session:
            with session.begin():
                item = session.get(ItemModel,item_id)
                session.delete(item)
                session.commit()

                return DeleteItemResponse(message="Item Deleted Successfully!")

class Mutation(graphene.ObjectType):
    createItem = AddItem.Field()
    editItem = EditItem.Field()
    deleteItem = DeleteItem.Field()