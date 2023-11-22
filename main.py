# import redis
# r = redis.Redis(host="127.0.0.1",port=6379,db=0)
# #r = redis.Redis(host='docker.for.win.localhost', port=6380,db=0)
# res = r.ping()
# if res :
#     # message ={
#     #     "school_2" : "hdu",
#     #     "year_2" : "2021",
#     #     "major_2" : "computer",
#     #     "sid_2" : "21052023",
#     #     "name_2" : "wsy"
#     # }
#     # r.mset(message)
#     print("success")
#     # m = r.mget("school_2","year_2","major_2","sid_2","name_2")
#     # print(m)
#
# else:
#     print("error")

'''import pymongo
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client["boss"]
collection = db["deep_learning"]
status = collection.delete_many({})
if status.acknowledged :
    print(1)'''

