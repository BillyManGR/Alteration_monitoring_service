from Crawler import create_links

#def monitoring(deep):
#     links = create_links()
#     for i in links:
#           for j in range(1, len(links[i])):
#             url = links[i][j]
#             id = DB_check(url)
#            if id>=0:       #exists
#                if deep:
#                    obj = parse(url)
#                    if DB_check(id, obj):
#                        continue
#                    populate(Recipes & Ingredients, Recipe, id, obj)        # modify
#            else:           # does not exist
#                obj = parse(url)
#                populate(Recipes & Ingredients, Recipe, O)                  # add