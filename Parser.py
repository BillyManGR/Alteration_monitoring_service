from Recipe import Recipe
from selenium import webdriver
import re, sys
from selenium.common.exceptions import NoSuchElementException


def time_unit_check(item):
    both_cond_en = "h" in item and "m" in item
    both_cond_el = ("ώρα" in item or "ώρες" in item or "ωρες" in item or "ωρα" in item) and\
                   ("λεπτά" in item or "λεπτα" in item or "λεπτό" in item or "λεπτό" in item)
    if "and" in item or "και" in item or both_cond_en or both_cond_el:
        return "both"
    if "week" in item or "εβδομάδες" in item or "εβδομάδα" in item:
        return "weeks"
    if "day" in item or "μέρες" in item or "μέρα" in item:
        return "days"
    try:
        return "minutes" \
            if "'" in item or "΄" in item or "\"" in item or "min" in item or "minutes" in item\
               or "mnutes" in item or "λεπτά" in item or "λεπτα" in item or float(item) >= 60 else "hours"
    except ValueError:      # item is in hours
        return "hours"


def extract_value(unit, item):                                  # Do not change the replace order
    # min = max = "0"
    if unit == "minutes":
        item = item.replace("΄", "")    # English unorthodox symbol for minutes
        item = item.replace("´", "")    # Greek unorthodox symbol for minutes
        item = item.replace("'", "")    # Yeah, they all have different ASCII code
        item = item.replace("\"", "")
        item = item.replace(" mnutes", "")
        item = item.replace(" minutes", "")
        item = item.replace(" mins", "")
        item = item.replace(" min", "")
        item = item.replace(" m", "")
        item = item.replace(" λεπτά", "")
        item = item.replace(" λεπτα", "")
    elif unit == "hours":
        item = item.replace(" hours", "")
        item = item.replace(" hrs", "")
        item = item.replace(" hour", "")
        item = item.replace(" h", "")
        item = item.replace(" ώρες", "")
        item = item.replace(" ωρες", "")
        item = item.replace(" ωρα", "")
        item = item.replace(" ώρα", "")
    elif unit == "days":
        item = item.replace(" days", "")
        item = item.replace(" day", "")
        item = item.replace(" μέρες", "")
        item = item.replace(" μέρα", "")
    else:
        item = item.replace(" weeks", "")
        item = item.replace(" week", "")
        item = item.replace(" εβδομάδες", "")
        item = item.replace(" εβδομάδα", "")
    item = item.replace(",", ".")
    if "-" in item:
        minimum = item.split("-")[0]
        maximum = item.split("-")[1]
    else:
        minimum = maximum = item
    return minimum, maximum


def get_final_value(item):
    # print("item: " + item)
    time_unit = time_unit_check(item)
    if time_unit == "minutes":                                              # item is minute
        # print("item '"+item+"' is minute")
        minimum, maximum = extract_value("minutes", item)                   # extract value
        min_value = float(minimum)
        max_value = float(maximum)
    elif time_unit == "days":                                              # item is days
        # print("item '"+item+"' is days")
        minimum, maximum = extract_value("days", item)                      # extract value
        min_value = float(minimum)*1440
        max_value = float(maximum)*1440
    elif item == "":                                                        # empty item
        # print("item '"+item+"' is empty")
        min_value = max_value = 0
    elif time_unit == "both":                                               # item is both minute and hour
        # print("item '"+item+"' is in both")
        items = item.split(" and ") if "and" in item else item.split(" και ")
        # print(items)
        if len(items) == 1:
            values = re.findall(r"[-+]?\d*\.\d+|\d+", item)
            # print(values)
            if len(values) == 1:                                            # Expected 2 values, got one
                sys.exit("Parsing error! Expected 2 values, got one!")
            else:
                minimum1, maximum1 = extract_value("hours", values[0])
                minimum2, maximum2 = extract_value("minutes", values[1])
                # print(minimum1, maximum1, minimum2, maximum2)
                min_value = float(minimum1)*60 + float(minimum2)
                max_value = float(maximum1)*60 + float(maximum2)
                # print("Min/Max value = "+str(min_value))
        else:
            min0, max0 = extract_value("hours", items[0])              # hour part
            min1, max1 = extract_value("minutes", items[1])               # minute part
            # print(min0, max0, min1, max1)
            min_value = float(min0)*60 + float(min1)                        # add values
            max_value = float(max0)*60 + float(max1)
    elif time_unit == "hours":                                              # item is hours
        # print("item '"+item+"' is is hours")
        minimum, maximum = extract_value("hours", item)
        min_value = float(minimum)*60
        max_value = float(maximum)*60
    else:                                                                   # item is weeks
        # print("item is weeks")
        minimum, maximum = extract_value("weeks", item)
        min_value = float(minimum)*10080
        max_value = float(maximum)*10080
    return min_value, max_value


def calculate_total_time(hands_on, hands_off, cook_time):
    hands_on_min, hands_on_max = get_final_value(hands_on)
    hands_off_min, hands_off_max = get_final_value(hands_off)
    cook_time_min, cook_time_max = get_final_value(cook_time)
    min_total_time = int(hands_on_min + hands_off_min + cook_time_min)
    max_total_time = int(hands_on_max + hands_off_max + cook_time_max)
    return min_total_time, max_total_time


def try_and_fix(raw):
    hands_on = hands_off = cook_time = portions = difficulty = ""
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
            print("Shitty HTML")
            del raw[i-1]
            hands_on, hands_off, cook_time, portions, difficulty = try_and_fix(raw)
    return hands_on, hands_off, cook_time, portions, difficulty


def extract_times(raw, lang):
    # print("initial raw: "+raw)
    if lang == "el":
        raw = raw.replace("Χρόνος\n", "Χρόνος ")
        raw = raw.replace("Βαθμός\n", "Βαθμός ")
        # print("Greek raw: "+raw)
    raw = raw.split("\n")
    raw = raw[:len(raw)-2]
    # print(raw)
    return try_and_fix(raw)


def get_diet(driver):
    diet = []
    labels = driver.find_element_by_class_name('list-inline.recipe-labels').find_elements_by_tag_name('li')
    for i in labels:
        diet.append(i.find_elements_by_tag_name('div')[0].get_attribute("class").split("label ")[1])
    return diet


def get_tags(driver):
    tags = []
    try:
        tag_series = driver.find_element_by_class_name('recipe-tags-wrap').find_elements_by_tag_name('li')
    except NoSuchElementException:                              # no tags
        print("No tags found")
        tag_series = []
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
        sys.exit("Error during get_method_ingredients_tip!")


def get_video(driver):
    try:
        return driver.find_element_by_class_name("media.ipad_media.hidden-xs").find_element_by_tag_name("source").get_attribute("src").split("src:_")[1]
    except NoSuchElementException:
        try:
            return driver.find_element_by_class_name("media.ipad_media.hidden-xs").find_element_by_tag_name("img").get_attribute("src")
        except NoSuchElementException:
            element = driver.find_element_by_class_name("media.ipad_media.hidden-xs")\
                .find_element_by_class_name("fb-video.fb_iframe_widget.fb_iframe_widget_fluid_desktop")
            href = element.get_attribute('data-href')
            return href


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
    # print(times_raw)
    hands_on, hands_off, cook_time, portions, difficulty = extract_times(times_raw, lang)
    total_time = get_total_time(hands_on, hands_off, cook_time)
    method = get_method_ingredients_tip(driver, "method")
    ingredients = get_method_ingredients_tip(driver, "ingredients")
    tip = get_method_ingredients_tip(driver, "tip")
    rating_value = driver.find_element_by_name("score").get_attribute("value")
    rating = 0 if rating_value == '' else float(rating_value)
    video = get_video(driver)
    driver.close()
    return Recipe(url, title, cat, diet, tags, hands_on, hands_off, cook_time, total_time, portions, difficulty, ingredients, method, tip, rating, video).convert_to_json()


# recipe = parse("https://akispetretzikis.com/el/categories/rofhmata-amp-pota/dark-n-stormy")
# recipe.simple_recipe_print()
# recipe.JSON_recipe_print()
# print(recipe)
