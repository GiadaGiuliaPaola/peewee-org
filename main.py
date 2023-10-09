import models
from peewee import *
from typing import List

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def cheapest_dish() -> models.Dish:
    """You want ot get food on a budget

    Query the database to retrieve the cheapest dish available
    """
    cheapest_dish = models.Dish.select().order_by(models.Dish.price_in_cents).get()
    return cheapest_dish

print('The price of the cheapest dish is:',cheapest_dish())

def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available
    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """
    vegeterian_ingredients_id = models.Ingredient.select().where(models.Ingredient.is_vegetarian == 1)
    
    is_vegetarian_list = models.Dish.select().where(
        ~models.Dish.id.in_(
            models.DishIngredient.select(models.DishIngredient.dish_id)
            .join(models.Ingredient)
            .where(~models.Ingredient.id.in_(vegeterian_ingredients_id))
        )
        # .distinct()
    )
    return list(is_vegetarian_list)

def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best
    Query the database to retrieve the restaurant that has the highest
    rating on average
    """
    query = (
        models.Rating.select(models.Restaurant, fn.AVG(models.Rating.rating).alias('avg_rating'))
        .join(models.Restaurant, on=(models.Rating.restaurant_id == models.Restaurant.id))
        .group_by(models.Restaurant)
        .order_by(SQL('avg_rating').desc())
        .limit(1)
    )

    top_rated_restaurant =query.first()

    return top_rated_restaurant


def add_rating_to_restaurant() -> None:
    """After visiting a restaurant, you want to leave a rating
    Select the first restaurant in the dataset and add a rating
    """
    create_rating = models.Rating.create(restaurant_id = 1 ,rating = 1)
    return create_rating


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """
    vegan_ingredients_id = models.Ingredient.select().where(models.Ingredient.is_vegan == 1)
    

    vegan_dish_ids = (
            models.DishIngredient.select(models.DishIngredient.dish_id)
            .join(models.Ingredient)
            .where(models.Ingredient.id.in_(vegan_ingredients_id))
            .group_by(models.DishIngredient.dish_id)
            .having(fn.COUNT(models.DishIngredient.ingredient_id)) == len(vegan_ingredients_id)
        )
    
    vegan_restaurant = (models.Restaurant
            .select()
            .join(models.Dish)
            .where(
                (models.Dish.id.in_(vegan_ingredients_id)) &
                (models.Restaurant.opening_time <= '19:00:00') &
                (models.Restaurant.closing_time <= '19:00:00')
            )
            .distinct()
    )

    return (vegan_restaurant)


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    cheese_ingredient = models.Ingredient.select().where(models.Ingredient.name == 'cheese').first()
    
    if not cheese_ingredient:
        cheese_ingredient = models.Ingredient.create(
            name='cheese',
            is_vegetarian = 1,
            is_vegan = 0,
            is_glutenfree = 0
        )
    new_dish = models.Dish.create(
        name = 'fondue',
        served_at_id = 1,
        price_in_cents = 1300
    )
    
    return new_dish


def print_numbered_dishes(dishes):
    for index, dish in enumerate(dishes, start=1):
        print(f"{index}. {dish.name}")

if __name__ == "__main__":
    vegetarian_dishes_list = vegetarian_dishes()
    print(vegetarian_dishes_list)
    print("The length of vegetarian dishes is:",len(vegetarian_dishes_list))
    print_numbered_dishes(vegetarian_dishes_list)

    best_rated_restaurant = best_average_rating()

    if best_rated_restaurant:
        print(f"The best-rated restaurant is: {best_rated_restaurant.restaurant.name}")
        print(f"Average Rating: {best_rated_restaurant.avg_rating:.2f}")
    else:
        print("No restaurants found in the database.")

    # add_rating_to_restaurant()


    possible_dinner_date_restaurants = dinner_date_possible()

    if possible_dinner_date_restaurants:
        print("Possible dinner date restaurants:")
        for restaurant in possible_dinner_date_restaurants:
            print(restaurant.name)
    else:
        print("No suitable restaurants found.")
    
    new_dish = add_dish_to_menu()
    print(f"New Dish Added: {new_dish.name}")

