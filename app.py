from fastapi import FastAPI
from routes import pdf_routes
import uvicorn
from multiprocessing import cpu_count

app = FastAPI()

# Include the PDF processing routes
app.include_router(pdf_routes)

# Optional root path
@app.get("/")
def root():
    return {"message": "FastAPI is running"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host="127.0.0.1", 
        port=8000, 
        log_level="info", 
        workers=cpu_count()
    )
