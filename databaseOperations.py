import pymongo
from bson import ObjectId


def insert_data(collection, data):
    document = collection.insert_one(data)
    return document.inserted_id


def get_collection():                     # CONNECT TO DATABASE
    client = pymongo.MongoClient('mongodb+srv://billy:grande@cookeapp-mhjnk.gcp.mongodb.net/test?retryWrites=true&w=majority')
    database = client.test
    database = client['Cooker']
    collection = database['Recipes']
    return client, collection


def update_or_create(collection, document_id, data):
    """
    This will create new document in collection
    IF same document ID exist then update the data
    :param collection:
    :param document_id:
    :param data:
    :return:
    """
    # TO AVOID DUPLICATES - THIS WILL CREATE NEW DOCUMENT IF SAME ID NOT EXIST
    document = collection.update_one({'_id': ObjectId(document_id)}, {"$set": data}, upsert=True)
    return document.acknowledged


def get_single_id(collection, attribute, value):
    """
    get document data by url
    :param collection:
    :param attribute:
    :param value:
    :return:
    """
    # print("Criterion: "+attribute)
    # print("Value: "+value)
    data = collection.find_one({attribute: value}) # TODO: Fix find_one. Explore more powerful options like find_one and replace
    return data.get('_id') if data is not None else None


# def get_multiple_data(collection):
    """
    get document data by document ID
    :param collection:
    :return:
    """
#     data = collection.find()
#     return list(data)


# def update_existing(document_id, data):
    """
    Update existing document data by document ID
    :param document_id:
    :param data:
    :return:
    """
    # document = collection.update_one({'_id': ObjectId(document_id)}, {"$set": data})
#  return document.acknowledged


# def remove_data(document_id):
    #     document = collection.delete_one({'_id': ObjectId(document_id)})
#    return document.acknowledged


def close_client(client):
    client.close()
