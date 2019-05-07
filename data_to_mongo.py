import pymongo

m_client = pymongo.MongoClient('mongodb://localhost:27017/')
m_db = m_client['db_ships']
m_collection = m_db['test']

r = list(m_collection.find())

print(r)