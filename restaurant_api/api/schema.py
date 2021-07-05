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
    