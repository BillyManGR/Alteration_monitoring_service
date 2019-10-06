from selenium import webdriver
import time, datetime, traceback, logging, sys
from databaseOperations import get_collection, close_client
from Monitoring import monitor
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
home = "https://akispetretzikis.com"
language = "Greek"


def find_recipes(driver, database, category):    # Find all the recipes of the given category
    driver.get(category)
    driver.save_screenshot("file_name.png")
    te = nsee = sere = ecie = 0    # exception counters
    while True:
        if driver.current_url != category:
            print("Current url != category")
            driver.get(category)
            time.sleep(1.5)
        try:
            time.sleep(0.5)
            driver.find_element_by_class_name('filter-select').click()
        except TimeoutException:
            te += 1
            print("TimeoutException: "+str(te))
            continue
        except NoSuchElementException:
            nsee += 1
            print("NoSuchElementException: "+str(nsee))
            break
        except StaleElementReferenceException:
            sere += 1
            print("StaleElementReferenceException: "+str(sere))
            # driver.save_screenshot("file_name Stale"+str(sere)+".png")
            continue
        except ElementClickInterceptedException:
            ecie += 1
            print("ElementClickInterceptedException")
            # driver.save_screenshot("file_name Intercepted"+str(ecie)+".png")
            continue
    sum_of_recipes = 1
    while True:
        try:
            time.sleep(0.4)
            first_recipe = driver.find_element_by_class_name("read_more").get_attribute("href")
            break
        except NoSuchElementException:
            print("Could not find first recipe")
            continue
    # print("First recipe: "+first_recipe)
    monitor(database, first_recipe)
    rest_recipes = driver.find_elements_by_class_name('more.hidden-xs')
    for x in rest_recipes:
        sum_of_recipes += 1
        print("Monitoring recipe no "+str(sum_of_recipes))
        monitor(database, x.get_attribute("href"))
    return sum_of_recipes
    

def crawl(lang):
    categories = []
    if lang == "Greek":
        categories_home = 'https://akispetretzikis.com/el/categories/p/kathgories-syntagwn'
    elif lang == "English":
        categories_home = 'https://akispetretzikis.com/en/categories/p/kathgories-syntagwn'
    else:
        sys.exit("Wrong language has been given for crawling. Choose either 'Greek' or 'English'")
    print(lang + " language has been chosen for crawling")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)  # options=options
    # driver = webdriver.Chrome()
    driver.get(categories_home)
    client, database = get_collection()
    for category in driver.find_elements_by_class_name('more'):
        categories.append(category.find_element_by_tag_name('a').get_attribute("href"))
    for current_category in categories:
        print("Current category: "+current_category)
        no_of_recipes = find_recipes(driver, database, current_category)
        print("Number of recipes of category " + current_category + " = " + str(no_of_recipes))
    driver.close()
    close_client(client)


start = datetime.datetime.now()
try:
    crawl(language)
except Exception as e:
    print("Did not end as expected")
    logging.error(traceback.format_exc())
end = datetime.datetime.now()
print("Monitoring time: " + str(end - start))
