from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_db():
    try:
        client = MongoClient(os.getenv("DB_URL"))
        print("connection established")
        return client
    except Exception as e:
        return f"faild connection {e}"