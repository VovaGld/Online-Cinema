# Online-Cinema


## Project Description


This project is a web application for an online cinema platform. It allows users to browse, search, buy and watch movies.
The application is built using the FastAPI framework. The database is managed using SQLAlchemy and PostgreSQL.

## Features


- **JWT authentication**
- **User registration and login**
- **Password reset functionality**
- **User profile management**
- **User roles (admin, user)**
- **Movie management (CRUD operations for admins)**
- **Movie search and filtering**
- **Movie rating and review system**
- **Cart management**
- **Order management**
- **Payment processing (using Stripe)**
- **Email notifications**

## How to Run the Project


Follow these steps to set up and run the **Online Cinema API** project on your local machine.


### **1. Clone the Repository**

Start by cloning the project repository from GitHub:

```bash
git https://github.com/VovaGld/Online-Cinema.git
cd online-cinema
```

---

### **2. Create and Activate a Virtual Environment**

It is recommended to use a virtual environment to isolate project dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

---

### **3. Install Dependencies with Poetry**

This project uses **Poetry** for dependency management. Install dependencies as follows:

```bash
# Install Poetry if not already installed
pip install poetry

# Install project dependencies
poetry install
```

---

### **4. Create a `.env` File**

Create a `.env` file in the project root directory with the following variables.
```bash
copy .env.example .env
```
Fill in the `.env` file with your database connection details and other necessary configurations.

---

### **5. Run the Docker Compose**
```bash
docker-compose -f docker-compose-local.yml up --build
```

---

### **6. Start the development server**:

```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```


