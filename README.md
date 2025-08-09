```bash

## 📂 Project Structure
FASTAPI/
│
├── app/
│ ├── init.py
│ ├── main.py # FastAPI app entry point
│ ├── models.py # SQLAlchemy models
│ ├── database.py # Database connection setup (SQLite)
│ ├── crud.py # CRUD operations
│ └── schemas.py # Pydantic models
│
├── requirements.txt
└── Procfile (for deployment)

yaml
Copy
Edit

```

## 🛠 Installation & Setup (Local)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
2. Create and activate a virtual environment
bash
Copy
Edit
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run the FastAPI application
bash
Copy
Edit
uvicorn app.main:app --reload
The API will be available at:

cpp
Copy
Edit
http://127.0.0.1:8000
📄 API Documentation
FastAPI automatically generates API documentation:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

🗄 Database
This project uses SQLite for local development.
The database file (crm.db) will be created automatically in the project directory when the app runs for the first time.

🧪 Example Endpoints
Create a Contact
POST /contacts/

json
Copy
Edit
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890"
}
Get All Contacts
GET /contacts/

Get a Single Contact
GET /contacts/{contact_id}

Update a Contact
PUT /contacts/{contact_id}

Delete a Contact
DELETE /contacts/{contact_id}

