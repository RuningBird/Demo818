from pymongo import MongoClient
import os
import get_ships
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
import hashlib

engine = create_engine('mysql+pymysql://root:1122@192.168.101.27:3306/db_ships')
# engine = create_engine('mysql+pymysql://root:1122@10.93.53.244/db_ships')  # company

all_ships = []

# ships_dir = '/home/hr/PycharmProjects/Demo818/test_data'
# ships_dir = '/home/hr/PycharmProjects/Demo818/ABERSHIP_transcription_vtls004566921'

# ships_dir = '/home/bbu/PycharmProjects/Demo818/ABERSHIP_transcription_vtls004566921/Series 461 - 470'
ships_dir = '/home/bbu/PycharmProjects/Demo818/ABERSHIP_transcription_vtls004566921'


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

        try:
            sql = '''REPLACE into z_all_ships_info values("{s_id}", "{vessel_name}", '{official_number} ', '{port_of_registry}', '{mariners}')'''.format(
                **df_dic)
            sess = Session(bind=engine)
            sess.execute(sql)
            sess.commit()

            mariners = elem["mariners"]
            mariners.to_sql(file_name_hash, con=engine, index=False, if_exists='replace')

            mariners.to_sql('z_all_members_info', con=engine, index=False, if_exists='append')
        except Exception as e:
            print(sql)
            raise e


files_path = []
for root, dirs, files in os.walk(ships_dir):
    for file in files:
        name, ext = os.path.splitext(file)
        if ext == '.xlsx':
            if '~' in file or 'Book' in file:
                continue
            files_path.append(os.path.join(root, file))


length = len(files_path)
for i in range(length):
    f = files_path[i]
    one_ships = get_ships.get_ships(f)
    data_to_sql(f, one_ships)

    if i > 400:
        break
    print('进度:{0}/{1}'.format(i + 1, length))

# print(files_path)
# print(len(files_path))
