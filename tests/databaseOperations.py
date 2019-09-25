import pymongo
from bson import ObjectId
from urllib.parse import urlparse


# CONNECT TO DATABASE
client = pymongo.MongoClient("mongodb+srv://billy:grande@cookeapp-mhjnk.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

# CREATE DATABASE
#database = connection['my_database']
# CREATE COLLECTION
#collection = database['my_collection']
db = client["sample_mflix"]
col = db["movies"]
movie = col.find_one({ "title": "Titanic", "year": 1997 })
print(movie)


def insert_data(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    document = collection.insert_one(data)
    return document.inserted_id


def update_or_create(document_id, data):
    """
    This will create new document in collection
    IF same document ID exist then update the data
    :param document_id:
    :param data:
    :return:
    """
    # TO AVOID DUPLICATES - THIS WILL CREATE NEW DOCUMENT IF SAME ID NOT EXIST
    document = collection.update_one({'_id': ObjectId(document_id)}, {"$set": data}, upsert=True)
    return document.acknowledged


def get_single_data(document_id):
    """
    get document data by document ID
    :param document_id:
    :return:
    """
    data = collection.find_one({'_id': ObjectId(document_id)})
    return data


def get_multiple_data():
    """
    get document data by document ID
    :return:
    """
    data = collection.find()
    return list(data)


def update_existing(document_id, data):
    """
    Update existing document data by document ID
    :param document_id:
    :param data:
    :return:
    """
    document = collection.update_one({'_id': ObjectId(document_id)}, {"$set": data})
    return document.acknowledged


def remove_data(document_id):
    document = collection.delete_one({'_id': ObjectId(document_id)})
    return document.acknowledged


# CLOSE DATABASE
client.close()