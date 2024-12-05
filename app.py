from flask import Flask
from routes import pdf_routes

app = Flask(__name__)

# Register the PDF processing routes
app.register_blueprint(pdf_routes)

if __name__ == "__main__":
    app.run(debug=True)
