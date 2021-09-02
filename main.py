import json
import pymongo
from tabulate import tabulate


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["UKFood"]
coll = db["Restaurants"]
#################################### Functions           ###########################################################

def selection1(cuisine,zipcode):
    query = {"FOODTYPE":cuisine, "ZIPCODE":zipcode}
    print(f"Restaurant Name\t\t\t\tAddress\t\t\t\t\t\t\tRating\n")
    for x in coll.find(query).sort("RATING",-1).limit(5):
        print(f"{x['RES_NAME']}\t\t{x['ADDRESS']}\t\t{x['RATING']}")

def selection2(address,rating):
    query_string= {'$regex' : address}
    condition = {'$gte' : rating}
    for x in coll.find({'ADDRESS': query_string,"RATING" : condition}).sort("RATING",-1):
        print(f"{x['RES_NAME']}   {x['FOODTYPE']}")

# def selection3(cuisine):
#     db.coll.aggregate([
#         {$match: { "FOODTYPE": cuisine }}
#         {$group: { "ZIPCODE": }}
#     ])
#     print(f"Restaurant Name\t\t\t\tAddress\t\t\t\t\t\t\tRating\n")
#     for x in coll.find(query).sort("RATING",-1).limit(5):
#         print(f"{x['RES_NAME']}\t\t{x['ADDRESS']}\t\t{x['RATING']}")


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
