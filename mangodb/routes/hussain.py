from fastapi import APIRouter
from bson import ObjectId
from confing.db_connection import get_db 
from models.hussain import Hussain_Add


hussain_route = APIRouter(prefix="/hussain", tags=["todo"])
client = get_db()
db = client["hussain_database"]

@hussain_route.get("/")
async def get_todo():
    try:
        collections = db.hussain.find()
        data = []
        for documnet in collections:
            data.append({
                "name":documnet["name"],
                "age":documnet["age"],
                "dept":documnet["dept"]
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
    
@hussain_route.get("/{id}")
async def get_todo(id:str):
    try:
        collections = db.hussain.find_one({"_id": ObjectId(id)})
        data = []
        for documnet in collections:
            data.append({
                "name":documnet["name"],
                "age":documnet["age"],
                "dept":documnet["dept"]
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
@hussain_route.post("/add")    
async def add_hussain(data:Hussain_Add):
    try:
        result = db.hussain.insert_one({
            "name":data.name,
            "age":data.age,
            "dept":data.dept
        })
        return{
            "data":{"_id": str(ObjectId(result.inserted_id))},
            "status":"success"
        }

    except Exception as e:
        return{
            "data":None,
            "message":str(e),
            "status":"error"
        }
