import json
import pymongo

## To Create The Database and Collection

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["UKFood"]
coll = db["Restaurants"]

# list to catch any duplicates
duplicates = []
restdict = {}
duplicates_rec = 0

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
    if jsonrow['name'] not in duplicates:
        restdict = {
            "RES_NAME"  : jsonrow["name"],
            "ADDRESS"   : str(jsonrow["address"]) +',' + jsonrow["address line 2"],
            "FOODTYPE"  : jsonrow["type_of_food"],
            "RATING"    : jsonrow["rating"],
            "ZIPCODE"   : jsonrow["outcode"] + jsonrow["postcode"]
        }
        coll.insert_one(restdict)
        duplicates.append(jsonrow['name'])
    else:
        duplicates_rec += duplicates_rec

print(f"Number of duplicate records removed :  {duplicates_rec}")
print(len(duplicates))