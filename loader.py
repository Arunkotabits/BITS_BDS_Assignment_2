import json
import pymongo

## To Create The Database and Collection

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["UKFood"]
coll = db["Restaurants"]

# list to catch any duplicates
duplicates = {}
restdict = {}

#Open and Read the JSON file.
#Load the data from file to DB
#Removed URL while loading into the collection
#Removed any duplicates
#Combined "Outcode" and "postcode" to get ZIP code
#Combined "address" and "address line 2" to address

with open('res.json') as data:
  for line in data:
    jsonrow = json.loads(line)
    # Removing the duplicated on the "Name" of the Restaurant.
    if (jsonrow['name'],jsonrow["outcode"] + jsonrow["postcode"]) not in duplicates.items():
        if jsonrow["rating"] != "Not yet rated": # Remove the records which do not have a rating yet
            restdict = {
                "RES_NAME"  : jsonrow["name"],
                "ADDRESS"   : str(jsonrow["address"]) +',' + jsonrow["address line 2"],
                "FOODTYPE"  : jsonrow["type_of_food"],
                "RATING"    : jsonrow["rating"],
                "ZIPCODE"   : jsonrow["outcode"] + jsonrow["postcode"]
            }
            coll.insert_one(restdict)
            duplicates[(jsonrow['name'])] = jsonrow["outcode"] + jsonrow["postcode"]
