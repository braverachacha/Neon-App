---
# NeonApp | Backend & Auth Study
---

A decoupled Full-Stack application focused on **JWT Authentication**, **SMTP integration**, and **API Architecture**.

##  Key Features
--- 
* **Stateless Auth:** Implemented via **JSON Web Tokens (JWT)**.
* **Email Verification:** Full account activation flow using **Flask-Mail (SMTP)**.
* **Database Agnostic:** Configured for **SQLite** (Dev) and **PostgreSQL** (Prod).
* **Decoupled Design:** Flask is used strictly as a REST API (no Jinja2/Static rendering).

## ️ Tech Stack
----

* **Backend:** Python / Flask / SQLAlchemy
* **Security:** PyJWT / Flask-JWT-Extended
* **Mailing:** Flask-Mail (TLS)
* **Environment:** Managed via `.env` (Database toggles & SMTP keys)

## Quick Start
---

1. **Setup Environment (.env):**

Clone the repo
```bash
git clone https://github.com/braverachacha/Neon-App.git

# Run the frontend folder
cd frontend
php -S localhost:8000 # or use VScode liveserver
```
----
Create `.env` file, copy all the code in `.env.example` file and fill all the necessary fields as instructed

2. **Run Backend:**
----

````bash
cd backend
# create and activate a virtual environment
python -m venv env 
source enc/bin/activate

# install all the required dependencies

pip install -r requirements.txt 
# run the application
python app.py
````
----
© All rights reserved. 2026  `♥BraveraTech♥`
----
