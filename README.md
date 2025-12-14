# Real time Task Management System

## Local setup - Backend

### 1. Setup virtual env and activate it
python -m venv venv \
venv/script/activate


### 2. clone the project
git clone https://github.com/AKSHAY-KR99/Real-time-task-management-system.git \
cd realtime-task-system

### 3. install dependencies
pip install -r requirements.txt \

### 4. setup .env file - .env located in root directory
MONGO_URL=mongodb://localhost:27017 \
MONGO_DB_NAME=tsm_db \
JWT_SECRET_KEY = "secrete_key" \
JWT_ALGORITHM = "HS256" \
ACCESS_TOKEN_EXPIRE_MINUTES = 30 \
CELERY_BROKER_URL=redis://localhost:6379/0 \
CELERY_RESULT_BACKEND=redis://localhost:6379/0 \
MAIL_PASSWORD=**password** \
MAIL_FROM=email@gmail.com

### 5. run the server
uvicorn app.main:app --reload


## Local setup - Front end

### 1. navigate to the folder
cd task-app-ui

### 2. install dependencies
npm install


### 3. run development server
npm run dev \
http://localhost:5173 or http://127.0.0.1:5173


### 4. Health Check
http://127.0.0.1:8000/health GET


### 5. Docker
run the command in root directory \
docker compose up --build


### Server URLs
FastAPI - http://127.0.0.1:8000/ \
Swagger - http://127.0.0.1:8000/docs \
React UI - http://127.0.0.1:5173/ \
MongoDB - mongodb://localhost:27017