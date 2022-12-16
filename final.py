import requests
from dotenv import load_dotenv
import os
import json
import webbrowser
import plotly.graph_objects as go

# import the secret keys for APIs
load_dotenv()
SPOONACULAR_KEY = os.getenv('SPOONACULAR_KEY')
GOOGLE_MAP_KEY = os.getenv('GOOGLE_MAP_KEY')
CACHE_FILENAME = "cache.json"

def open_cache():
    '''try to read the cached data in the cache file

    Returns
    -------
    dictionary
        the cached data that can be load as a nested dictionary

    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict, filename):
    '''save the tree dictionary in the cache file

    Parameters
    ----------
    cache_dict: dictionary
        nested dictionary that contains the tree structure and data
    filename: string
        the name of the cache file

    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(filename,"w")
    fw.write(dumped_json_cache)
    fw.close()

def clean_input(user_input):
    '''clean the user input data for the ingredients and construct unique key for caching

    Parameters
    ----------
    user_input: string
        user's input string

    Returns
    -------
    string
        cleaned input string that can be used as a unique key for caching
    '''
    input_list = user_input.strip().split(",")
    res = []
    for ingredient in input_list:
        res.append(ingredient.strip().lower())
    res.sort()
    return "_".join(res)

def check_input(res):
    '''check the user input to determine yes or no

    Parameters
    ----------
    res: string
        user's input string

    Returns
    -------
    bool
        True if the user's answer is yes, False otherwise

    '''
    possible_yes = ['yes', 'y', 'yup', 'sure', 'yeah']
    possible_no = ['no', 'nah', 'not', 'none', 'n', 'nope']
    while res.lower() not in possible_yes and res.lower() not in possible_no:
        res = input('Please answer yes or no: ')
    return True if res.lower() in possible_yes else False

def call_api(base_url, params):
    '''call the api using provided url info and return the response results

    Parameters
    ----------
    base_url: string
        the base url string
    params: dictionary
        the parameters for the url

    Returns
    -------
    dictionary
        the results in a dictionary
    '''
    response = requests.get(base_url, params)
    return response.json()

def plot_restaurant(values):
    '''use the restaurant data to plot a table for a better visulization,
        and the table will be presented in the browser

    Parameters
    ----------
    values: list
        a nested list that represents the column data for the table

    '''
    print("Displaying results in your browser...")
    fig = go.Figure(data=[go.Table(
    columnorder = [1, 2, 3, 4, 5],
    columnwidth = [5, 10, 20, 40, 10],
    header = dict(
        values = [['<b>ID</b>'],
                  ['<b>Rating</b>'],
                  ['<b>Name</b>'],
                  ['<b>Address</b>'],
                  ['<b>Price Level</b>']],
        line_color='darkslategray',
        fill_color='royalblue',
        font=dict(color='white', size=12),
        height=40
    ),
    cells=dict(
        values=values,
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white']),
        font_size=12,
        height=30)
        )
    ])
    fig.show()

def construct_restaurants(values):
    '''construct the column data for the restaurant table and plot the table

    Parameters
    ----------
    values: dictionary
        a dictionary that represents the detailed data for each restaurant

    Returns
    -------
    dictionary
        a dictionary that shows the relationship between the table id and the restaurant place id

    '''
    restaurant_id = []
    rating_col = []
    name_col = []
    address_col = []
    price_col = []
    cnt = 0
    relationship_dict = {}
    for name, info in values.items():
        cnt += 1
        restaurant_id.append(cnt)
        rating_col.append(info["rating"])
        name_col.append(name)
        address_col.append(info["address"])
        price_col.append(info["price level"])
        relationship_dict[str(cnt)] = info["place id"]
    plot_restaurant([restaurant_id, rating_col, name_col, address_col, price_col])
    return relationship_dict

def plot_recipe(values):
    '''use the recipe data to plot a table for a better visulization,
        and the table will be presented in the browser

    Parameters
    ----------
    values: list
        a nested list that represents the column data for the table

    '''
    print("Displaying detailed results in your browser...")
    fig = go.Figure(data=[go.Table(
    columnorder = [1, 2, 3, 4],
    columnwidth = [40, 100, 400, 400],
    header = dict(
        values = [['<b>ID</b>'],
                  ['<b>Name</b>'],
                  ['<b>Used Ingredients</b>'],
                  ['<b>Missed Ingredients</b>']],
        line_color='darkslategray',
        fill_color='royalblue',
        font=dict(color='white', size=12),
        height=40
    ),
    cells=dict(
        values=values,
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white']),
        font_size=12,
        height=30)
        )
    ])
    fig.show()

def construct_recipes(values):
    '''construct the column data for the recipe table and plot the table

    Parameters
    ----------
    values: dictionary
        a dictionary that represents the detailed data for each recipe

    '''
    id_col = []
    name_col = []
    used_col = []
    missed_col = []
    for id, info in values.items():
        id_col.append(id)
        name_col.append(info["name"])
        used_col.append([" " + " ".join(ingredent) for ingredent in info["used ingredients"]])
        missed_col.append([" " + " ".join(ingredent) for ingredent in info["missed ingredients"]])
    plot_recipe([id_col, name_col, used_col, missed_col])

# check if the cache file exist
total_cache = open_cache()

first_choice = input("Hi, what do you want to do today?\n1. make yourself a meal\n2. find a restaurant near you\nPlease choose 1 or 2 from the above options: ")
while not first_choice.isdigit() or int(first_choice) < 1 or int(first_choice) > 2:
    first_choice = input("Please enter either 1 or 2 as the choice: ")

if first_choice == "1":
    recipes_content = total_cache.get("recipes", {})
    searched_recipes_content = recipes_content.get("searched recipes", {})
    detailed_recipes_content = recipes_content.get("detailed recipes", {})
    ingredients = input("Please enter ingredients in your refrigerator (separate by comma): ")
    clean_ingredients = clean_input(ingredients)
    find_by_ingredients_url = 'https://api.spoonacular.com/recipes/findByIngredients'
    find_by_ingredients_params = {
        "ingredients": ingredients,
        "apiKey": SPOONACULAR_KEY
    }

    # check the cache to see if it contains the requested data
    target_recipes = searched_recipes_content.get(clean_ingredients, {})

    # if the requested ingredient combination is not a child of "searched recipes", call the API for the new data
    if not target_recipes:
        this_recipes = call_api(find_by_ingredients_url, find_by_ingredients_params)

        for recipe in this_recipes:
            recipe_id = str(recipe["id"])
            recipe_name = recipe["title"]
            used_ingredients = [(str(ingre["amount"]), ingre["unit"], ingre["name"]) for ingre in recipe["usedIngredients"]]
            missed_ingredients = [(str(ingre["amount"]), ingre["unit"], ingre["name"]) for ingre in recipe["missedIngredients"]]
            target_recipes[recipe_id] = {"name": recipe_name, "used ingredients": used_ingredients, "missed ingredients": missed_ingredients}
        searched_recipes_content[clean_ingredients] = target_recipes

    # show the recipe results by construct a table using plotly
    construct_recipes(target_recipes)

    is_continue = True
    while is_continue:
        recipe_choice = input("Please enter the recipe id that you want to know more about: ")
        while recipe_choice not in target_recipes:
            recipe_choice = input("Please enter a valid recipe id in the table: ")

        # if the recipe id is not a child of "detailed recipes", call the API for detailed recipe data
        if recipe_choice not in detailed_recipes_content:
            detailed_recipe_url = f"https://api.spoonacular.com/recipes/{recipe_choice}/information"
            detailed_recipe_params = {
                "apiKey": SPOONACULAR_KEY
            }
            this_detail = call_api(detailed_recipe_url, detailed_recipe_params)
            detailed_title = this_detail["title"]
            detailed_url = this_detail["spoonacularSourceUrl"]
            detailed_recipes_content[recipe_choice] = {"title": detailed_title, "url": detailed_url}

        # Internet connection needed for displaying detailed recipe info
        print("Open the detailed results in your browser...")
        webbrowser.open(detailed_recipes_content[recipe_choice]["url"])

        is_continue = check_input(input("Do you want to see another detailed recipe? (yes/no) "))

    # update the cache dictionary for searched recipe and detailed recipe data
    recipes_content["searched recipes"] = searched_recipes_content
    recipes_content["detailed recipes"] = detailed_recipes_content
    total_cache["recipes"] = recipes_content

else:

    # read the existing restaurant and location data from the cache file
    restaurants_content = total_cache.get("restaurants", {})
    location_content = total_cache.get("locations", {})

    is_continue = True
    while is_continue:

        # first question: location
        print("What's your current location?")
        tmp_dict = {}
        no_res = 0
        for idx, location in enumerate(location_content):
            tmp_dict[str(idx)] = location
            print(idx, ":", location)
            no_res = idx + 1
        print(no_res, ": None of above")
        location_input = input("Please choose your current location from the list above: ").strip()
        while not location_input.isdigit() or int(location_input) < 0 or int(location_input) > no_res:
            location_input = input("Please enter a valid choice: ").strip()
        if location_input == str(no_res):
            location_input = input("Please enter your current location: ").strip().lower()
        else:
            location_input = tmp_dict[location_input]

        if not location_content:
            total_cache["locations"] = {}
        target_location = location_content.get(location_input, {})   # target_location = lat,lng

        # if this location isn't a child of "locations", call the API for new location data
        if not target_location:
            google_map_find_place_base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            google_map_find_place_params = {
                "input": location_input,
                "inputtype": "textquery",
                "fields": "geometry",
                "key": GOOGLE_MAP_KEY
            }

            location_results = call_api(google_map_find_place_base_url, google_map_find_place_params)["candidates"][0]
            lat, lng = location_results["geometry"]["location"]["lat"], location_results["geometry"]["location"]["lng"]
            target_location = f"{lat},{lng}"
            location_content[location_input] = target_location
            restaurants_content[location_input] = {}   # this must be the first time searching this location

        # second question: prefered cuisine type
        print("What kind of meal do you like?")
        tmp_dict = {}
        no_res = 0
        for idx, cuisine in enumerate(restaurants_content[location_input]):
            tmp_dict[str(idx)] = cuisine
            print(idx, ":", cuisine)
            no_res = idx + 1
        print(no_res, ": None of above")
        cuisine_input = input("Please choose your prefered cuisine type from the list above: ").strip().lower()
        while not cuisine_input.isdigit() or int(cuisine_input) < 0 or int(cuisine_input) > no_res:
            cuisine_input = input("Please enter a valid choice: ").strip()
        if cuisine_input == str(no_res):
            cuisine_input = input("Please enter your prefered cuisine type: ").strip().lower()
        else:
            cuisine_input = tmp_dict[cuisine_input]


        target_cuisine = restaurants_content[location_input].get(cuisine_input, {})

        # if the target cuisine type is not a child of current location node, call the API for new restaurant data
        if not target_cuisine:
            google_map_text_search_base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            google_map_text_search_params = {
                "query": cuisine_input,
                "location": target_location,
                "radius": 10000,
                "key": GOOGLE_MAP_KEY
            }
            restaurant_results = call_api(google_map_text_search_base_url, google_map_text_search_params)["results"]

            restaurant_dict = {}
            for restaurant in restaurant_results:
                this_name = restaurant["name"]
                this_address = restaurant["formatted_address"]
                this_geometry = restaurant["geometry"]["location"]
                price_level = restaurant.get("price_level", None)
                this_rating = restaurant.get("rating", {})
                place_id = restaurant.get("place_id", {})
                restaurant_dict[this_name] = {"address": this_address, "geo location": this_geometry, "price level": price_level, "rating": this_rating, "place id": place_id}

            # construct the rating children of this cuisine type
            target_cuisine["greater 4.5"] = {}
            target_cuisine["4-4.5"] = {}
            target_cuisine["less 4"] = {}
            for restaurant, info in restaurant_dict.items():
                if info["rating"]:
                    if float(info["rating"]) > 4.5:
                        target_cuisine["greater 4.5"][restaurant] = info
                    elif float(info["rating"]) < 4:
                        target_cuisine["less 4"][restaurant] = info
                    else:
                        target_cuisine["4-4.5"][restaurant] = info
            restaurants_content[location_input][cuisine_input] = target_cuisine

        middle_is_continue = True
        while middle_is_continue:
            # third question: rating range
            print("What rating range do you prefer?")
            print("1 : greater than 4.5")
            print("2 : 4.0 to 4.5")
            print("3 : less than 4.0")
            rating_input = input("Please choose your prefered rating range from the list above: ").strip().lower()
            while not rating_input.isdigit() or int(rating_input) > 3 or int(rating_input) < 1:
                rating_input = input("Please enter a valid choice: ").strip()

            # construct table for visulization
            if rating_input == "1":
                relationship_dict = construct_restaurants(target_cuisine["greater 4.5"])
            elif rating_input == "3":
                relationship_dict = construct_restaurants(target_cuisine["less 4"])
            else:
                relationship_dict = construct_restaurants(target_cuisine["4-4.5"])


            inner_is_continue = True
            while inner_is_continue:
                # view the detail of a specific restaurant (Internet needed for open the webpage)
                if not relationship_dict:
                    print("There is no restaurants in this rating range.")
                    break
                restaurant_choice = input("Which restaurant do you want to know more about? ")
                while restaurant_choice not in relationship_dict:
                    restaurant_choice = input("Please enter a valid restaurant id from the table: ")

                restaurant_place_id = relationship_dict[restaurant_choice]

                # because the url info is not in the previous place searching response, so we need to call the api for the url and display detailed information
                google_map_detailed_info_base_url = "https://maps.googleapis.com/maps/api/place/details/json"
                google_map_detailed_info_params = {
                    "place_id": restaurant_place_id,
                    "fields": "url",
                    "key": GOOGLE_MAP_KEY
                }
                detailed_restaurant_results = call_api(google_map_detailed_info_base_url, google_map_detailed_info_params)["result"]

                # Internet connection needed for displaying detailed restaurant info
                print("Open the detailed results in your browser...")
                webbrowser.open(detailed_restaurant_results["url"])
                inner_is_continue = check_input(input("Do you want to check another restaurant's detail? (yes/no): "))
            middle_is_continue = check_input(input("Do you want to check another rating range? (yes/no): "))
        is_continue = check_input(input("Do you want to search for another cuisine types? (yes/no): "))

    # update the cache for restaurants and locations
    total_cache["restaurants"] = restaurants_content
    total_cache["locations"] = location_content

# save the updated cache
save_cache(total_cache, CACHE_FILENAME)