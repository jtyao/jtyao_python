import pymongo
import sys

MONGO_URL = 'localhost'
MONGO_DB = 'football_odds'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def save_to_mongo(match):
    """
    保存至MongoDB
    :param result: 结果
    """
    if (match['league']):
        collection = db[match['league']]
    else:
        print("存储数据错误")
        sys.exit()
    print(collection)
    result = collection.find_one({'year': match['year'], 'date': match['data'],})
#result = collection.find_one({'year': match['year'], 'date': match['data'], 'home_name':match['home_name']})
    print(result)
    while(1):
        a = 0

    try:
        if result:
            print("数据重复")
            return
        else:
            print("数据存储")
            if collection.insert(match):
                print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')

def save_match(match):
    save_to_mongo(match)
