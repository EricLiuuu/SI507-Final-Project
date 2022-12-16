from treelib import Tree
import json
CACHE_FILENAME = "cache.json"


# This file can display the current tree structure in the cache file,
# but it doesn't contain data on the leaf nodes.
# It makes use of the treelib library for the tree visulization purpose.
# The real (functional) tree is implemented by nested dictionaries in the 'final.py' file.
# The tree structure will be printed in the terminal.

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

tree_content = open_cache()
if tree_content:
    tree = Tree()
    tree.create_node("Root", "root")
    tree.create_node("Recipes", "recipes", parent="root")
    tree.create_node("Restaurants", "restaurants", parent="root")
    tree.create_node("Locations", "locations", parent="root")

    # create location tree
    locations = tree_content.get("locations", {})
    for location, geometry in locations.items():
        tree.create_node(location, None, parent="locations")

    # create recipe tree
    recipes = tree_content.get("recipes", {})
    if recipes:
        searched_recipes = recipes.get("searched recipes", {})
        detailed_recipes = recipes.get("detailed recipes", {})
        tree.create_node("Searched Recipes", "searched recipes", parent="recipes")
        tree.create_node("Detailed Recipes", "detailed recipes", parent="recipes")
        for search_query, results in searched_recipes.items():
            tree.create_node(search_query, search_query, parent="searched recipes")
            for res, val in results.items():
                tree.create_node(val["name"], None, parent=search_query)
        for detailed_id, info in detailed_recipes.items():
            tree.create_node(info["title"], None, parent="detailed recipes")

    # create restaurant tree
    restaurants = tree_content.get("restaurants", {})
    location_cnt = 0
    cuisine_cnt = 100
    rating_cnt = 1000
    for location, cuisines in restaurants.items():
        location_cnt += 1
        tree.create_node(location, location_cnt, parent="restaurants")
        for cuisine, rating in cuisines.items():
            cuisine_cnt += 1
            tree.create_node(cuisine, cuisine_cnt, parent=location_cnt)
            for rating, results in rating.items():
                rating_cnt += 1
                tree.create_node(rating, rating_cnt, parent=cuisine_cnt)
                for name, info in results.items():
                    tree.create_node(name, None, parent=rating_cnt)
    tree.show()