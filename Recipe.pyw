from datetime import datetime,timedelta, date
class Recipe:
    
    def __init__(self, url, title, category, diet, tags, hands_on, hands_off, cook_time, total_time, portions, difficulty, ingredients, method, tip, rating, video_or_image):
        self.url = url
        self.title = title                                              # string
        self.category = category
        self.diet = diet
        self.tags = tags
        self.hands_on = hands_on
        self.hands_off = hands_off
        self.cook_time = cook_time
        self.total_time = total_time
        self.portions = portions
        self.difficulty = difficulty
        self.ingredients = ingredients
        self.method = method
        self.tip = tip
        #self.nut_chart = nut_chart
        self.rating = rating
        self.video_or_image = video_or_image                                              # video url

    def simple_recipe_print(self):
        print("URL: "+self.url)
        print("Title: " + self.title)
        print("Category: " + self.category)
        print("Diet: ", end='')
        print(self.diet)
        print("Tags: ", end='')
        print(self.tags)
        print("Hands on: " + self.hands_on + "\nHands off: " + self.hands_off + "\nCook time: " + self.cook_time + "\nPortions: " + self.portions + "\nDifficulty: " + self.difficulty)
        print("Total time: " + self.total_time)
        print("Method: \n" + self.method)
        print("\nIngredients:")
        print(self.ingredients)
        print("Tip: " + self.tip)
        print("Rating: " + str(self.rating))
        print("Video: " + self.video_or_image)
        # Pending nutrition 
    
    def JSON_recipe_print(self):
        print(serialize(self))

    def convert_to_JSON(self):
        return serialize(self)

def serialize(obj):
    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial
    return obj.__dict__