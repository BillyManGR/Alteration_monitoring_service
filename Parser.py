from Recipe import Recipe
from selenium import webdriver
import re, sys
from selenium.common.exceptions import NoSuchElementException


def time_unit_check(item):
    both_cond_en = ("hour" in item or "hours" in item) and "minutes" in item
    both_cond_el = ("ώρα" in item or "ώρες" in item) and "λεπτά" in item
    if "and" in item or "και" in item or both_cond_en or both_cond_el:
        return "both"
    try:
        return "minutes" if "'" in item or "min" in item or "minutes" in item or "λεπτά" in item or float(item) >= 60 else "hours"            
    except ValueError:      # item is in hours
        return "hours"


def extract_minute_value(minute, item):
    # min = max = "0"
    if minute:
        item = item.replace("'", "")
        item = item.replace(" minutes", "")
        item = item.replace(" min", "")
        item = item.replace(" λεπτά", "")
    else:
        item = item.replace(" hours", "")
        item = item.replace(" hrs", "")
        item = item.replace(" hour", "")
        item = item.replace(" ώρες", "")
    item = item.replace(",", ".")
    return item.split("-") if "-" in item else item, item


def get_final_value(item):
    # print("item: " + item)
    time_unit = time_unit_check(item)
    if time_unit == "minutes":                                              # item is minute
        # print("item is minute")
        minimum, maximum = extract_minute_value(True, item)                 # extract value
        min_value = float(minimum)
        max_value = float(maximum)
    elif item == "":                                                        # empty item
        # print("Item is empty")
        min_value = max_value = 0
    elif time_unit == "both":                                               # item is both minute and hour
        # print("Item in both")
        items = item.split(" and ") if "and" in item else item.split(" και ")
        # print(items)
        if len(items) == 1:
            values = re.findall(r"[-+]?\d*\.\d+|\d+", item)
            print(values)
            if len(values) == 1:                                            # Expected 2 values, got one
                sys.exit("Parsing error! Expected 2 values, got one!")
            else:
                min_value = max_value = float(values[0])*60 + float(values[1])
                # print("Min/Max value = "+str(min_value))
        else:
            min0, max0 = extract_minute_value(False, items[0])              # hour part
            min1, max1 = extract_minute_value(True, items[1])               # minute part
            min_value = float(min0)*60 + float(min1)                        # add values
            max_value = float(max0)*60 + float(max1)
    else:                                                           # item is hours
        # print("item is hours")
        minimum, maximum = extract_minute_value(False, item)
        min_value = float(minimum)*60
        max_value = float(maximum)*60
    return min_value, max_value


def calculate_total_time(hands_on, hands_off, cook_time):
    hands_on_min, hands_on_max = get_final_value(hands_on)
    hands_off_min, hands_off_max = get_final_value(hands_off)
    cook_time_min, cook_time_max = get_final_value(cook_time)
    min_total_time = int(hands_on_min + hands_off_min + cook_time_min)
    max_total_time = int(hands_on_max + hands_off_max + cook_time_max)
    return min_total_time, max_total_time
         

def extract_times(raw, lang):
    hands_on = hands_off = cook_time = portions = difficulty = ""
    # print("initial raw: "+raw)
    if lang == "el":
        raw = raw.replace("Χρόνος\n", "Χρόνος ")
        raw = raw.replace("Βαθμός\n", "Βαθμός ")
        # print("Greek raw: "+raw)
    raw = raw.split("\n")
    raw = raw[:len(raw)-2]
    # print(raw)
    for i in range(1, len(raw), 2):
        # print(i)
        if raw[i] == "Ηands on" or raw[i] == "Χρόνος Εκτέλεσης":
            hands_on = raw[i-1]
        elif raw[i] == "Hands off" or raw[i] == "Χρόνος Αναμονής":
            hands_off = raw[i-1]
        elif raw[i] == "Cook Time" or raw[i] == "Χρόνος Ψησίματος":
            cook_time = raw[i-1]
        elif raw[i] == "Portion(s)" or raw[i] == "Μερίδες":
            portions = raw[i-1]
        elif raw[i] == "Difficulty" or raw[i] == "Βαθμός Δυσκολίας":
            difficulty = raw[i-1]
        else:
            print("Error while extracting times!")
    return hands_on, hands_off, cook_time, portions, difficulty


def get_diet(driver):
    diet = []
    labels = driver.find_element_by_class_name('list-inline.recipe-labels').find_elements_by_tag_name('li')
    for i in labels:
        diet.append(i.find_elements_by_tag_name('div')[0].get_attribute("class").split("label ")[1])
    return diet


def get_tags(driver):
    tags = []
    tag_series = driver.find_element_by_class_name('recipe-tags-wrap').find_elements_by_tag_name('li')
    for i in range(1, len(tag_series)):
        tags.append(tag_series[i].text)
    return tags


def get_total_time(hands_on, hands_off, cook_time):
    min_total_time, max_total_time = calculate_total_time(hands_on, hands_off, cook_time)
    if min_total_time == max_total_time:
        return str(max_total_time) + "'"
    else:
        return str(min_total_time) + "' - " + str(max_total_time) + "'"


def get_method_ingredients_tip(driver, option):
    elements = driver.find_elements_by_class_name("text")
    method = elements[1].text
    # print("len(elements) = " + str(len(elements)))
    tip = elements[2].text if len(elements) == 4 else ""
    ingredients_raw = elements[0].text
    ingredients = ingredients_raw.split("\n")
    if option == "method":
        return method
    elif option == "ingredients":
        return ingredients
    elif option == "tip":
        return tip
    else:
        print("error during get_method_ingredients_tip")


def get_video(driver):
    try:
        return driver.find_element_by_class_name("media.ipad_media.hidden-xs").find_element_by_tag_name("source").get_attribute("src").split("src:_")[1]
    except NoSuchElementException:
        return driver.find_element_by_class_name("media.ipad_media.hidden-xs").find_element_by_tag_name("img").get_attribute("src")


def parse(url):
    lang = "en" if "/en/" in url else "el"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    title = driver.find_element_by_tag_name('h1').text
    cat = driver.find_element_by_class_name('recipe-breadcrumb').text.split("/ ",1)[1]
    diet = get_diet(driver)
    tags = get_tags(driver)
    times_raw = driver.find_element_by_class_name("new-times").text
    hands_on, hands_off, cook_time, portions, difficulty = extract_times(times_raw, lang)
    total_time = get_total_time(hands_on, hands_off, cook_time)
    method = get_method_ingredients_tip(driver, "method")
    ingredients = get_method_ingredients_tip(driver, "ingredients")
    tip = get_method_ingredients_tip(driver, "tip")
    rating = float(driver.find_element_by_name("score").get_attribute("value"))
    video = get_video(driver)
    driver.close()
    return Recipe(url, title, cat, diet, tags, hands_on, hands_off, cook_time, total_time, portions, difficulty, ingredients, method, tip, rating, video)


# recipe = parse("https://akispetretzikis.com/el/categories/zymarika/zymarika-me-keftedakia-galopoylas")
# recipe.simple_recipe_print()
# recipe.JSON_recipe_print()
# print(recipe.convert_to_JSON())
