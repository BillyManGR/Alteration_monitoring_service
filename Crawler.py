from selenium import webdriver
import time, datetime, traceback, logging, sys
from databaseOperations import get_collection, close_client
from Monitoring import monitor
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

home = "https://akispetretzikis.com"
#language = "English"
#first = True


def show_more_recipes(driver, page):
    te = nsee = sere = ecie = 0  # exception counters
    can_show_more = True
    if driver.current_url != page:
        print("Current url != category")
        driver.get(page)
        time.sleep(1.5)
    try:
        time.sleep(0.5)
        driver.find_element_by_class_name('filter-select').click()
        time.sleep(0.2)
    except TimeoutException:
        te += 1
        print("TimeoutException: " + str(te))
        show_more_recipes(driver, page)
    except NoSuchElementException:
        nsee += 1
        print("NoSuchElementException: " + str(nsee))
        can_show_more = False
    except StaleElementReferenceException:
        sere += 1
        print("StaleElementReferenceException: " + str(sere))
        # driver.save_screenshot("file_name Stale"+str(sere)+".png")
        show_more_recipes(driver, page)
    except ElementClickInterceptedException:
        ecie += 1
        print("ElementClickInterceptedException")
        # driver.save_screenshot("file_name Intercepted"+str(ecie)+".png")
        show_more_recipes(driver, page)
    return can_show_more


def find_first_recipe(driver):
    while True:  # Get the first recipe of the page
        try:
            time.sleep(0.4)
            first_recipe = driver.find_element_by_class_name("read_more").get_attribute("href")
            break
        except NoSuchElementException:
            print("Could not find first recipe")
            continue
    print("Monitoring recipe no 1")
    return first_recipe


def find_recipes(driver, database, page, lite):  # Find recipes of the given page
    driver.get(page)
    sum_of_recipes = 1
    print("Crawling page: " + page)
    first_recipe = find_first_recipe(driver)
    exists = monitor(database, first_recipe)
    if exists and lite:
        return 0  # No new recipes
    else:
        seen_recipes = []
        can_show_more = True
        while can_show_more:
            rest_recipes = driver.find_elements_by_class_name(
                'more.hidden-xs')  # Gather the currently visible recipes
            for x in rest_recipes:  # Go through the currently visible recipes
                current_recipe = x.get_attribute("href")
                if current_recipe in seen_recipes:  # Already seen that. Next!
                    continue
                sum_of_recipes += 1
                print("Monitoring recipe no " + str(sum_of_recipes))
                exists = monitor(database, current_recipe)
                seen_recipes.append(current_recipe)
                if exists and lite:
                    return sum_of_recipes - 1  # No need to continue with the rest of the recipes (Current recipe is not new)
            can_show_more = show_more_recipes(driver, page)  # Can you show more recipes?
        return sum_of_recipes


def deep_crawl(lang, driver, database):
    if lang == "Greek":
        categories_home = 'https://akispetretzikis.com/el/categories/p/kathgories-syntagwn'
    elif lang == "English":
        categories_home = 'https://akispetretzikis.com/en/categories/p/kathgories-syntagwn'
    else:
        sys.exit("Wrong language has been given for crawling. Choose either 'Greek' or 'English'")
    print("Deep crawling in " + lang)
    driver.get(categories_home)
    categories = []
    for category in driver.find_elements_by_class_name('more'):
        categories.append(category.find_element_by_tag_name('a').get_attribute("href"))
    for current_category in categories:
        print("Current category: " + current_category)
        no_of_recipes = find_recipes(driver, database, current_category, False)
        print("Number of recipes of category " + current_category + " = " + str(no_of_recipes))


def lite_crawl(lang, driver, database):
    if lang == "Greek":
        new_recipes = 'https://akispetretzikis.com/el/recent-recipes'
    elif lang == "English":
        new_recipes = 'https://akispetretzikis.com/en/recent-recipes'
    else:
        sys.exit("Wrong language has been given for crawling. Choose either 'Greek' or 'English'")
    print("Lite crawling in " + lang)
    no_of_recipes = find_recipes(driver, database, new_recipes, True)
    print("Number of new recipes: " + str(no_of_recipes))


def crawl(lang, first_time):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)  # options=options
    # driver = webdriver.Chrome()
    client, database = get_collection()
    if first_time:
        deep_crawl(lang, driver, database)
    else:
        lite_crawl(lang, driver, database)
    driver.close()
    close_client(client)


def automated_crawling(language, first):
    start = datetime.datetime.now()
    try:
        crawl(language, first)
    except Exception as e:
        print("Did not end as expected")
        logging.error(traceback.format_exc())
    end = datetime.datetime.now()
    print("Monitoring time: " + str(end - start))
