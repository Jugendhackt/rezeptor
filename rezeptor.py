from flask import Flask, jsonify, request, render_template
import re
import unidecode
import neuralnetwork


# create the app. This variable named jh constains our app
jh = Flask(__name__)

ingredients = [
    ["Tomato", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/%22farmer%27s_market%22_%282617703671%29.jpg/800px-%22farmer%27s_market%22_%282617703671%29.jpg", 1, "g"],
    ["Onions", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Red_onion_rings_closeup.jpg/120px-Red_onion_rings_closeup.jpg"],
    ["Potatoes", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/181008-N-OA516-0011.jpg/120px-181008-N-OA516-0011.jpg"],
    ["Olives", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/El_Perell%C3%B3_-_Old_olive_tree.jpg/800px-El_Perell%C3%B3_-_Old_olive_tree.jpg"],
    ["Cheese", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Camembert.JPG/1024px-Camembert.JPG"],
    ["Capsicum", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Aligned_peperonis.JPG/800px-Aligned_peperonis.JPG"],
    ["Chillies", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Camembert.JPG/1024px-Camembert.JPG"],
    ["Ginger", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Knoblauch_Bluete_3.JPG/1024px-Knoblauch_Bluete_3.JPG"],
    ["Garlic", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Knoblauch_Bluete_3.JPG/1024px-Knoblauch_Bluete_3.JPG"],
    ["Sugar", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Raw_cane_sugar_light.JPG/1024px-Raw_cane_sugar_light.JPG"],
    ["Milk", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Israeli_Milk_Bag.jpg/1024px-Israeli_Milk_Bag.jpg"],
    ["Bread", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Breads.jpg/1024px-Breads.jpg"],
    ["Salt", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/France_salin_de_giraud_salt_mountain.jpg/500px-France_salin_de_giraud_salt_mountain.jpg"],
    ["Choco-Chips", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Choco_chip_cookie_half.png/1024px-Choco_chip_cookie_half.png"]
]

# add routes to our app
@jh.route('/')
def Rezeptor():
    out=[]
    for i in range(len(ingredients)):
        out.append(ingredients[i].append(slugify(ingredients[i][0])))
    return render_template('frontpage.html', ingredients=ingredients )

@jh.route('/recipe', methods=['GET', 'POST'])
def test():
    form = request.form
    ingredientsAvailable = []
    ingredientsBinary = []
    for ingred in ingredients:
        slug = slugify(ingred[0])
        try:
            form[slug]
        except:
            ingredientsAvailable.append(slug)
            ingredientsBinary.append(1)
        else:
            ingredientsBinary.append(0)

    return render_template('recipe.html')
    return jsonify(neuralnetwork.dieAI(ingredientsBinary))

@jh.route('/test2')
def test2():
    return render_template('testpage.html')

def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)


# This comment a comment
# Run the app if someone runs this file.
if __name__ == "__main__":
    jh.run(debug=True)
