from fastapi import FastAPI
from pydantic import BaseModel
from confing.db_connection import get_db

client = get_db()
db = client["hussain_database"]

app = FastAPI()

@app.get("/")
async def get():
    try:
        collection = db.hussain.find()
        data = []
        for document in collection:
            data.append({
                "name":document["name"],
                "age":document["age"],
                "dept":document["dept"]
            })
        return{
            "data":data,
            "status":"success"
        }

    except Exception as e:
        return{
            "data":None,
            "message":str(e),
            "status":"error"
        }    