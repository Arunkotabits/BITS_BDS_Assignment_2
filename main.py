import json
import pymongo
from tabulate import tabulate
from prettytable import PrettyTable


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["UKFood"]
coll = db["Restaurants"]

#################################### Functions           ###########################################################

def selection1(cuisine,zipcode):
    query = {"FOODTYPE":cuisine, "ZIPCODE":zipcode}
    myTable = PrettyTable(['RES_NAME', 'ADDRESS', 'RATING'])
    for x in coll.find(query).sort("RATING",-1).limit(5):
        myTable.add_row([x['RES_NAME'],x['ADDRESS'], x['RATING']])
    print(myTable)

def selection2(address,rating):
    query_string= {'$regex' : address}
    condition = {'$gte' : rating}
    myTable = PrettyTable(['RES_NAME', 'FOODTYPE'])
    for x in coll.find({'ADDRESS': query_string,"RATING" : condition}).sort("RATING",-1):
        myTable.add_row([x['RES_NAME'],   x['FOODTYPE']])
    print(myTable)

def selection3(cusine):
    agg_result = coll.aggregate([
        { '$match' : { 'FOODTYPE': cusine}},
        { '$group' : { '_id' : '$ZIPCODE', 'count' : { '$sum': 1}}},
        { '$sort'   : {'count' : -1}}
    ])
    myTable = PrettyTable(['ZIPCODE', 'Count'])
    for record in agg_result:
        myTable.add_row([record["_id"], record["count"]])
    print(myTable)

def selection4():
    agg_result = coll.aggregate([
        { '$group' : { '_id' : '$FOODTYPE', 'count': {'$avg' : '$RATING'}}},
        { '$sort'   : {'count' : -1}}
    ])
    myTable = PrettyTable(['Food Type', 'Average Rating'])
    for record in agg_result:
        myTable.add_row([record["_id"],record["count"]])
    print(myTable)


################################### Input From the User:############################################################
print("Enter Your Selection: \n" 
        "1. Search by Cuisine and Zipcode.\n" 
        "2. Search by Address and Rating.\n" 
        "3. Number of Restaurants by Cusine and Zipcode\n" 
        "4. Average Rating by fodd type\n")

user_selection = int(input("Select The Number :"))

if user_selection == 1:
    cuisine = input("Enter the cuisine you are looking for : ")
    zipcode = input("Enter The Zipcde  ")
    selection1(cuisine, zipcode)
elif user_selection == 2:
    address = input("Enter the partial address you would like to search on : ")
    rating = float(input("Enter the minimum rating:  "))
    selection2(address, rating)
elif user_selection == 3:
    cuisine = input("Enter the cuisine you are looking for : ")
    selection3(cuisine)
else:
    selection4()

####################################################################################################################
