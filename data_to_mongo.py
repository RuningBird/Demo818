from pymongo import MongoClient
import pandas as pd
import hashlib
import json
import os

import get_ships


class MongoBase:
    def __init__(self, collection):
        self.collection = collection
        self.OpenDB()

    def OpenDB(self):
        user = 'root'
        passwd = '123'
        # host = 'localhost'
        host = '106.12.108.158'
        port = '27017'
        auth_db = 'admin'
        uri = "mongodb://" + user + ":" + passwd + "@" + host + ":" + port + "/" + auth_db
        # uri = "mongodb://" + user + ":" + passwd + "@" + host + ":" + port + "/" + auth_db + "?authMechanism=SCRAM-SHA-1"
        self.con = MongoClient(uri, connect=False)
        self.db = self.con['db_ships']
        self.collection = self.db[self.collection]

    def closeDB(self):
        self.con.close()


def insert_df_to_mongo(df=pd.DataFrame(), collection_name=None):
    mongo = MongoBase(collection_name)
    mongo.collection.insert(json.loads(df.T.to_json()).values())
    mongo.closeDB()


def insert_dict_to_mongo(doc=None, collection_name=None):
    mongo = MongoBase(collection_name)
    mongo.collection.insert(doc)
    mongo.closeDB()


def data_to_sql(file_name="", one_ships=[]):
    file_name_hash = 's_' + hashlib.md5(file_name.encode('utf8')).hexdigest()
    for elem in one_ships:
        df_dic = {
            "s_id": file_name_hash,
            "vessel_name": elem["vessel_name"],
            "official_number": elem["official_number"],
            "port_of_registry": elem["port_of_registry"],
            "mariners": file_name_hash,
        }

        mariners = elem["mariners"]
        try:
            # 船只信息总表
            insert_dict_to_mongo(doc=df_dic, collection_name='z_all_ships_info')

            # 船只人员信息入库
            insert_df_to_mongo(mariners, file_name_hash)

            # 人员信息总表
            insert_df_to_mongo(mariners, 'z_all_members_info')

        except Exception as e:
            print(e)
            # raise e


if __name__ == '__main__':
    # 批处理：设置文件夹路径
    # ships_dir = '/home/hr/PycharmProjects/Demo818/test_data'
    # ships_dir = '/home/hr/PycharmProjects/Demo818/ABERSHIP_transcription_vtls004566921'
    # ships_dir = '/home/bbu/PycharmProjects/Demo818/ABERSHIP_transcription_vtls004566921/Series 461 - 470'
    ships_dir = '/home/bbu/PycharmProjects/Demo818/ABERSHIP_transcription_vtls004566921'

    # 生成文件列表
    files_path = []
    for root, dirs, files in os.walk(ships_dir):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext == '.xlsx':
                if '~' in file or 'Book' in file:
                    continue
                files_path.append(os.path.join(root, file))

    # 文件诸葛存入数据库
    length = len(files_path)
    for i in range(length):
        f = files_path[i]
        try:
            one_ships = get_ships.get_ships(f)
            data_to_sql(f, one_ships)
        except Exception as e:
            print(e)

        if i > 400:
            break
        print('进度:{0}/{1}'.format(i + 1, length))
