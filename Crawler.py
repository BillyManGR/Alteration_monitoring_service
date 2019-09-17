from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import pprint
home = "https://akispetretzikis.com"

def find_recipes(driver, i, category, links):                                           #i = ith category, category = the category link, links = 2D matrix with all the links of the categories and all recipe links for each category 
    driver.get(category)
    #show all results
    te = nsee = sere = 0
    while(True):
        try:
            # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Show more recipes")))
            driver.find_element_by_link_text('Show more recipes').click()
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
            continue
    # populate the links
    first_recipe = (driver.find_element_by_link_text('Read more')).get_attribute("href")
    print("First recipe: "+first_recipe)
    links[i].append(first_recipe)
    # print(first_recipe)
    rest_recipes = driver.find_elements_by_link_text('more')
    for x in rest_recipes:
        links[i].append(x.get_attribute("href"))
    

def create_links():
    links = [[]]
    categories_home = 'https://akispetretzikis.com/en/categories/p/kathgories-syntagwn'
    driver = webdriver.Chrome()
    driver.get(categories_home)
    number_of_categories = len(driver.find_elements_by_link_text('more'))
    for i in range(0, number_of_categories):
        driver.get(categories_home)
        category_links = driver.find_elements_by_link_text('more')
        current_category = category_links[i].get_attribute("href")
        print("Current category: "+current_category)
        links[i].append(current_category)
        find_recipes(driver, i,current_category,links)
        print("Number of recipes: "+str(len(links[i])-1))
        if i != number_of_categories-1:
            links.append([])
    driver.close()
    return links

def pretty_print(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

#links = create_links()
#pretty_print(links)
#print(links)