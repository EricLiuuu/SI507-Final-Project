# SI507 Final Project - "What to Eat Today" APP
Highlights: Google Places API, Spoonacular API, Data Structure - Tree, Caching, Interactive Command Line Tool
## Discription
As a master's student, I always find it difficult to come up with ideas for “what to eat” in my daily life. The academic work and research tasks have already exhausted me, so I really don’t have time to think about what to eat for lunch or dinner.

As a result, I would like to build an application that can help people come up with ideas about what to eat. Users can input the ingredients that they currently have, and the system can provide them with some relative recipes (find recipes by ingredients). They have the option to see the details of those recipes that they are interested in. If they are not satisfied with any of those recipes, they also have the choice to search for nearby restaurants. The system can provide nearby restaurant information based on user's input, which will indicate the user’s preference for location, cuisine type, and rating range.

The application makes use of a tree structure to handle users' choices. All the data will be stored in the leaf node of the tree. Based on different choices, the algorithm will go into different branches of the tree and display corresponding results to the users. 

### Files
* `final.py` is the main file of this project. It contains all the necessary functions that run the program.  
* `cache.json` is the cache file that can be updated each time the users run the program. I store the cache data as a tree structure in this file.
* `read_tree.py` is an auxiliary file that contains the code for reading the tree structure in the cache file. It makes use of the `treelib` library.

## Usage
Run the `final.py` file:
```
Hi, what do you want to do today?
1. make yourself a meal
2. find a restaurant near you
Please choose 1 or 2 from the above options: 1
```
### If we choose to make a meal...

The program will ask for users to make a choice in the terminal. Here we choose to make a meal.
```
Please enter ingredients in your refrigerator (separate by comma): egg, potato, tomato, cheese
```
We enter the ingredients that we currently have. for example: `egg, potato, tomato, cheese`

Then we can see the table of recipes in our browser：
<p align="center" width="100%">
    <img width="100%" src="Docs/recipe_table.PNG">
</p>

```
Displaying detailed results in your browser...
Please enter the recipe id that you want to know more about: 633224
```

And now we want to see the detail of recipe "Baby Brie-Topped Potato Slices" with id "633224", so we enter "633224" in the command line.

Here is the detailed recipe opened in the browser:

<p align="center" width="100%">
    <img width="50%" src="Docs/spoon.PNG">
</p>

```
Open the detailed results in your browser...
Do you want to see another detailed recipe? (yes/no) no
```

If you want to see another detailed recipe, please enter yes here.

### If we choose to find a restaurant...
```
What's your current location?
0 : ann arbor
1 : lansing
2 : canton
3 : None of above
Please choose your current location from the list above: 0
```
The list above comes from the cache file. It represents a split of the tree. Searched results will be cached each time the program calls the API. If none of above is your location, choose the "None of above" option and enter your current location. Here we just go with the first choice.
```
What kind of meal do you like?
0 : japanese cuisine
1 : chinese cuisine
2 : mediterranean cuisine
3 : indian cuisine
4 : seafood restaurant
5 : None of above
Please choose your prefered cuisine type from the list above: 0
```
The cuisine type list here also comes from the cache, and this choice represents a split of the tree as well. If none of above fits your need, please choose "None of above" and enter your prefered cuisine type. We choose the first option here.
```
What rating range do you prefer?
1 : greater than 4.5
2 : 4.0 to 4.5
3 : less than 4.0
Please choose your prefered rating range from the list above: 1
```
The rating range choices here split the tree one more time. All the "japanese cuisine" restaurants in "ann arbor" are divided into three categories. Here we choose the first option.

<p align="center" width="100%">
    <img width="100%" src="Docs/restaurant_table.PNG">
</p>

