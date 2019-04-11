from flask import Flask, jsonify, request, render_template
import re
import unidecode
import neuralnetwork


# create the app. This variable named jh constains our app
jh = Flask(__name__)

ingredients = []
ingredientList = [
    ["Tomato", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/%22farmer%27s_market%22_%282617703671%29.jpg/800px-%22farmer%27s_market%22_%282617703671%29.jpg", 300, "grams"],
    ["Onions", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Red_onion_rings_closeup.jpg/120px-Red_onion_rings_closeup.jpg", 75, "grams"],
    ["Olives", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/El_Perell%C3%B3_-_Old_olive_tree.jpg/800px-El_Perell%C3%B3_-_Old_olive_tree.jpg", 50  , "grams"],
    ["Cheese", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Camembert.JPG/1024px-Camembert.JPG", 120, "grams"],
    ["Potatoes", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/181008-N-OA516-0011.jpg/120px-181008-N-OA516-0011.jpg", 200, "grams"],
    ["Capsicum", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Aligned_peperonis.JPG/800px-Aligned_peperonis.JPG", 2, "pcs"],
    ["Chillies", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Camembert.JPG/1024px-Camembert.JPG", 3, "pcs"],
    ["Ginger", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Starr_070730-7818_Zingiber_officinale.jpg/800px-Starr_070730-7818_Zingiber_officinale.jpg", 1, "grams"],
    ["Garlic", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Knoblauch_Bluete_3.JPG/1024px-Knoblauch_Bluete_3.JPG", 4, "Cloves"],
    ["Sugar", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Raw_cane_sugar_light.JPG/1024px-Raw_cane_sugar_light.JPG", 3, "Table-spoon"],
    ["Milk", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Israeli_Milk_Bag.jpg/1024px-Israeli_Milk_Bag.jpg", 120, "ml"],
    ["Bread", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Breads.jpg/1024px-Breads.jpg", 7, "pcs"],
    ["Salt", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/France_salin_de_giraud_salt_mountain.jpg/500px-France_salin_de_giraud_salt_mountain.jpg", 2, "Table-spoon"],
    ["Choco-Chips", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Choco_chip_cookie_half.png/1024px-Choco_chip_cookie_half.png", 50, "grams"]
]

class Ingredient():
    def __init__(self, name, image, multiplier, unit, calculated=0):
        self.name = name
        self.image = image
        self.multiplier = multiplier
        self.unit = unit
        self.calculated = calculated
        self.slug = slugify(self.name)

# add routes to our app
@jh.route('/')
def Rezeptor():
    return render_template('frontpage.html', ingredients=ingredients )

@jh.route('/recipe', methods=['GET', 'POST'])
def test():
    form = request.form
    ingredientsAvailable = []
    ingredientsBinary = []
    for ingredient in ingredients:
        try:
            form[ingredient.slug]
        except:
            ingredientsAvailable.append(ingredient.slug)
            ingredientsBinary.append(1)
        else:
            ingredientsBinary.append(0)
    nnOut = neuralnetwork.dieAI(ingredientsBinary)
    genRecipe = []
    for i in range(len(ingredients)):
        if nnOut[i] > 0.5:
            ingredient = ingredients[i]
            ingredient.calculated = int(round(nnOut[i]*ingredient.multiplier))
            genRecipe.append(ingredient)

    #return jsonify(recipe)
    return render_template('recipe.html', recipe=genRecipe)
    return jsonify(neuralnetwork.dieAI(ingredientsBinary))

def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)


# This comment a comment
# Run the app if someone runs this file.
if __name__ == "__main__":
    for ingred in ingredientList:
        ingredients.append(Ingredient(ingred[0],ingred[1],ingred[2],ingred[3]))
    jh.run(debug=True,host='0.0.0.0')
