import sys
from Parser import parse
from databaseOperations import get_single_id, update_or_create


def monitor(database, url):         #Monitors a recipe
    print("Monitoring url: "+url)
    obj_id = get_single_id(database, "url", url)
    print(obj_id)
    if obj_id is None:
        recipe = parse(url)
        # print(recipe)
        tries = 0
        while True:
            successful = update_or_create(database, obj_id, recipe)
            tries += 1
            if not successful:
                print("Updating or creating '" + recipe.__getitem__("title") + "' entry was not "
                    + "successful after "+str(tries)+" tries. Max 3 tries. Trying again")
                if tries == 3:
                    sys.exit("Max 3 failed tries reached! Aborting!")
                else:
                    continue
            else:
                print("Updating or creating '" + recipe.__getitem__("title")
                      + "' entry was successful after " + str(tries) + " tries")
                break
        return False
    else:
        return True

# client, collection = get_collection()
# monitor(collection, "https://akispetretzikis.com/en/categories/glykes-pites-tartes/pitakia-me-tachini")
# close_client(client)
