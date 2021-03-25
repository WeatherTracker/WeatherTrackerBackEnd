from pymongo import MongoClient
import json

client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
db = client.station
def write_database():
    with open('CWS_2Days.json', 'r', encoding="utf-8") as f:
        # 把json檔为dict
        json_data = json.load(f)
        ask=json_data["location"]
        district=json_data["district"]
        # for i in range(len(ask)):
        print(district)
    try:
        # myquery = {"city": "基隆市"}  # 查询条件
        # self.collection.update_one(myquery, data, upsert=True)  # upsert=True不存在则插入，存在则更新

        db.keelung.update_one(
            {"city": "基隆市"},
            {"$set": {
                "locations": ask
            }}, upsert=True
        )
        # self.collection.insert(data)
        print('寫入成功')
    except Exception as e:
        print(e)
    # def read_datebase( self ):
    #     try:
    #         myquery = {"city": "基隆市"} # 查询条件
    #         scene_flow = self.collection.find(myquery)
    #         print(type(scene_flow))
    #         for x in scene_flow:
    #             print(type(x))
    #             print(x)
    #         print ('讀取成功')
    #     except Exception as e:
    #         print (e)


if __name__ == '__main__':
    # jm = Json2Mongo()
    write_database()
    # jm.read_datebase()
