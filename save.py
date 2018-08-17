import pymongo
import sys
import config

MONGO_URL = 'localhost'
MONGO_DB = 'football_odds'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def save_match(match):
    """
    保存至MongoDB
    :param result: 结果
    """
    if (match['league']):
        collection = db[match['league']]
    else:
        print("存储数据错误")
        sys.exit()

    try:
        #if collection.insert(match):
            print('存储到MongoDB成功')
            config.match_total += 1
    except Exception:
        print('存储到MongoDB失败')

def get_exist_state(match):
    if (match['league']):
        collection = db[match['league']]
    else:
        print("存储数据错误")
        sys.exit()

    result = collection.find_one({'year': match['year'], 'date': match['date'], 'home_name':match['home_name']})
    if result:
        print("数据重复")
        return 'existed'
