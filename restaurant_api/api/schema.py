# from typing_extensions import Required
from django.db.models import query
import graphene

from graphene_django import DjangoObjectType, DjangoListField

from .models import Food

class FoodType(DjangoObjectType):
    class Meta:
        model = Food
        fields = "__all__"

class Query(graphene.ObjectType):
    all_foods = graphene.List(FoodType)
    food = graphene.Field(FoodType, food_id=graphene.Int())

    def resolve_all_foods(self,info, **kwargs):
        return Food.objects.all()
    def resolve_food(self, info, food_id):
        return Food.objects.get(id=food_id)

class FoodInput(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    type = graphene.String()
    price = graphene.Float()
    fastingFood = graphene.Boolean()

class CreateFood(graphene.Mutation):
    class Arguments:
        food_data = FoodInput(required=True)
    food = graphene.Field(FoodType)
    @staticmethod
    def mutate(root, info, food_data=None):
        food_inistance = Food(name=food_data.name, description=food_data.description, type=food_data.type, price=food_data.price, fastingFood = food_data.fastingFood)
        food_inistance.save()
        return CreateFood(food=food_inistance)

class Mutation(graphene.ObjectType):
    create_food = CreateFood.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)