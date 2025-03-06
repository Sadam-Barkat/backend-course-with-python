# poetry add python-multipart
from fastapi import FastAPI,File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import shutil
import os


app = FastAPI()

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

UPLOAD_FOLDER = "E:/backend_course/file_handling/uploads"  # Define the folder to store uploaded files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mount the uploads folder to serve static files
app.mount("/static", StaticFiles(directory=UPLOAD_FOLDER), name="static")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return the public URL to access the file
    file_url = f"/static/{file.filename}"

    return {"filename": file.filename, "file_url": file_url}