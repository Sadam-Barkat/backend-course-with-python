from backend import db_helper
from pydantic import BaseModel, ValidationError, EmailStr, Field
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request


app = FastAPI()

class Expense(BaseModel):
    expense_date:str
    amount:int
    category:str
    notes:str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(map(str, error["loc"])),  # Converts tuple path to a string
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "Validation failed",
            "errors": errors
        }
    )



@app.get("/hello")
def get_expenses():
    try:
        expenses = db_helper.fetch_all_records()
        data = []
        for expense in expenses:
            data.append(
            {
                "id": expense["id"],
                "expense_date": expense["expense_date"],
                "amount": expense["amount"],
                "category": expense["category"],
                "note": expense["notes"]
            })
        return {
            "data": data,
            "status": "success"
        }
    except Exception as e:
        return {
            "data": None,
            "message": str(e),
            "status": "error"
        }

@app.post("/insert_expense")  
def post(expense:Expense):
    try:
        result = db_helper.insert_expense(expense.expense_date, expense.amount, expense.category, expense.notes)
        return{
            "data":result,
            "status":"success",
        }
    except Exception as e:
        return{
            "data":None,
            "message":str(e),
            "status":"error"
        }


