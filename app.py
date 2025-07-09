from fastapi import FastAPI
from routes import pdf_routes

app = FastAPI()

# Include the PDF processing routes
app.include_router(pdf_routes)

# Optional root path
@app.get("/")
def root():
    return {"message": "FastAPI is running"}
