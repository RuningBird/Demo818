from pymongo import MongoClient
import os
import get_ships
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
import hashlib

engine = create_engine('mysql+pymysql://root:1122@192.168.101.27:3306/db_ships')

all_ships = []

# ships_dir = '/home/hr/PycharmProjects/Demo818/test_data'
ships_dir = '/home/hr/PycharmProjects/Demo818/ABERSHIP_transcription_vtls004566921'


def data_to_sql(file_name="", one_ships=[]):
    file_name_hash = hashlib.md5(file_name.encode('utf8')).hexdigest()
    for elem in one_ships:
        df_dic = {
            "s_id": file_name_hash,
            "vessel_name": elem["vessel_name"],
            "official_number": elem["official_number"],
            "port_of_registry": elem["port_of_registry"],
            "mariners": file_name_hash,
        }

        sql = '''REPLACE into z_all_ships_info values('{s_id}', '{vessel_name}', '{official_number} ', '{port_of_registry}', '{mariners}')'''.format(
            **df_dic)
        sess = Session(bind=engine)
        sess.execute(sql)
        sess.commit()

        mariners = elem["mariners"]
        mariners.to_sql(file_name_hash, con=engine, index=False, if_exists='replace')

        mariners.to_sql('z_all_members_info', con=engine, index=False, if_exists='append')

        # mariners_df_dict = {
        #     'name': [],
        #     'year_of_birth': [],
        #     'age': [],
        #     'place_of_birth': [],
        #     'home_address': [],
        #     'last_ship_name': [],
        #     'last_ship_port': [],
        #     'last_ship_leaving_date': [],
        #     'this_ship_joining_date': [],
        #     'this_ship_joining_port': [],
        #     'this_ship_capacity': [],
        #     'this_ship_leaving_date': [],
        #     'this_ship_leaving_port': [],
        #     'this_ship_leaving_cause': [],
        #     'signed_with_mark': [],
        #     'additional_notes': []
        # }
        #
        # for e in mariners:
        #     mariners_df_dict['name'].append(e.get('name'))
        #     mariners_df_dict['year_of_birth'].append(e.get('year_of_birth'))
        #     mariners_df_dict['age'].append(e.get('age'))
        #     mariners_df_dict['place_of_birth'].append(e.get('place_of_birth'))
        #     mariners_df_dict['home_address'].append(e.get('home_address'))
        #     mariners_df_dict['last_ship_name'].append(e.get('last_ship_name'))
        #     mariners_df_dict['last_ship_port'].append(e.get('last_ship_port'))
        #     mariners_df_dict['last_ship_leaving_date'].append(e.get('last_ship_leaving_date'))
        #     mariners_df_dict['this_ship_joining_date'].append(e.get('this_ship_joining_date'))
        #     mariners_df_dict['this_ship_joining_port'].append(e.get('this_ship_joining_port'))
        #     mariners_df_dict['this_ship_capacity'].append(e.get('this_ship_capacity'))
        #     mariners_df_dict['this_ship_leaving_date'].append(e.get('this_ship_leaving_date'))
        #     mariners_df_dict['this_ship_leaving_port'].append(e.get('this_ship_leaving_port'))
        #     mariners_df_dict['this_ship_leaving_cause'].append(e.get('this_ship_leaving_cause'))
        #     mariners_df_dict['signed_with_mark'].append(e.get('signed_with_mark'))
        #     mariners_df_dict['additional_notes'].append(e.get('additional_notes'))
        #
        # df_table = pd.DataFrame(mariners_df_dict)
        # df_table.to_sql(file_name_hash, con=engine, index=False, if_exists='replace')


files_path = []
for root, dirs, files in os.walk(ships_dir):
    for file in files:
        name, ext = os.path.splitext(file)
        if ext == '.xlsx':
            if '~' in file or 'Book' in file:
                continue
            files_path.append(os.path.join(root, file))
            # one_ships = get_ships.get_ships(os.path.join(root, file))
            # all_ships += one_ships

            # data_to_sql(file, one_ships)

length = len(files_path)
for i in range(length):
    f = files_path[i]
    one_ships = get_ships.get_ships(f)
    data_to_sql(f, one_ships)
    print('进度:{0}/{1}'.format(i + 1, length))

# print(files_path)
# print(len(files_path))
