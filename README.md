# KOTUMA
# ⚖️ Legal Aid Web App

The Legal Aid Web App is a platform designed to connect users with legal professionals, simplify access to legal information, and enable efficient management of legal aid services. This application is built with **FastAPI** on the backend and supports future frontend integration.

---

## 🚀 Features

- 🧑‍⚖️ User Registration and Authentication (OAuth2 + JWT)
- 📄 Legal Document Submission
- 🗂 Case Assignment and Tracking
- 📬 Contact and Messaging with Legal Experts
- 🔍 Search and Filter for Legal Topics
- ✅ Role-based Access Control (Admin, Lawyer, User)
- 🔒 Secure API with token-based authentication

---

## 🛠 Tech Stack

| Layer        | Technology     |
|--------------|----------------|
| Backend      | FastAPI        |
| ORM / Models | SQLModel / SQLAlchemy |
| Database     | Supabase (PostgreSQL) |
| Auth         | OAuth2 + JWT   |
| Environment  | Python 3.10+   |
| Deployment   | (Optional) Docker / Railway / Render |

---

---

## ⚙️ Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/naecherem20/KOTUMA.git
cd KOTUMA

## Create and activate virtual environment**
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows

## Install Dependencies
pip install -r requirements.txt

## Create a .env file in the root folder
DATABASE_URL=postgresql+psycopg2://postgres:<password>@db.<your-project>.supabase.co:5432/postgres

 ## Runserver**
uvicorn app.main:app --reload

## Testing
pytest


