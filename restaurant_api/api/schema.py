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

class UpdateFood(graphene.Mutation):
    class Arguments:
        food_data = FoodInput(required=True)
    food = graphene.Field(FoodType)

    @staticmethod
    def mutate(root, info, food_data=None):
        food_instance = Food.objects.get(id=food_data.id)

        if food_instance:
            food_instance.name = food_data.name
            food_instance.description = food_data.description
            food_instance.type = food_data.type
            food_instance.price = food_data.price
            food_instance.fastingFood = food_data.fastingFood
            food_instance.save()
            return UpdateFood(food=food_instance)
        return UpdateFood(food=None)

        
class DeleteFood(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    food = graphene.Field(FoodType)

    @staticmethod
    def mutate(root, info, id):
        food_instance = Food.objects.get(pk=id)
        food_instance.delete()

        return None

class Mutation(graphene.ObjectType):
    create_food = CreateFood.Field()
    update_food = UpdateFood.Field()
    delete_food = DeleteFood.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)