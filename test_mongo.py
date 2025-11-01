from pymongo import MongoClient

# Local MongoDB URI
MONGO_URI = "mongodb://localhost:27017/ev_database"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["ev_database"]

# List collections (should be empty initially)
print("Collections in database:", db.list_collection_names())
