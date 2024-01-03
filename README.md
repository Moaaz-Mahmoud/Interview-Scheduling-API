# Interview Scheduling API

This project is an API designed to manage interview records efficiently 
through a RESTful service. It provides endpoints for creating, retrieving,
updating, and deleting interview entries. Each interview record includes 
information such as interviewee name, interviewer name, interview datetime,
duration, and status.


## Features

- **Create Interview:** Add a new interview record with details like interviewee name, interviewer name, date, and duration.
- **Retrieve Interview:** Get details of a specific interview by its unique identifier.
- **Update Interview:** Modify the details of an existing interview, including interviewee name, interviewer name, date, duration, and status.
- **Delete Interview:** Remove a specific interview record from the system.
- **List Interviews:** Retrieve a list of all interviews, including relevant details.

## Technologies Used

- **Flask:** A lightweight web framework for building the API.
- **Flask-RESTful:** An extension for Flask that simplifies API development.
- **SQLAlchemy:** A SQL toolkit and Object-Relational Mapping (ORM) library for interacting with the database.
- **SQLite:** A simple, serverless relational database engine.

## Getting Started

1. Clone the repository

```
git clone https://github.com/Moaaz-Mahmoud/Interview-Scheduling-API
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Run the database creation script

```python3 create_db.py``` (Linux)

```python create_db.py``` (Windows)

4. Run the database seed script

```python3 seed_db.py``` (Linux)

```python seed_db.py``` (Windows)

5. Run the application: 

```python3 run.py``` (Linux)

```python3 run.py``` (Windows)

6. Access the API at http://localhost:5000/interviews

## API Endpoints and Methods

- **GET /interviews:** Retrieve a list of all interviews.
- **GET /interviews/{id}:** Get details of a specific interview.
- **POST /interviews:** Create a new interview record.
- **PATCH /interviews/{id}:** Update an existing interview record.
- **DELETE /interviews/{id}:** Delete a specific interview record.

## Example Requests

### 1. Create a New Interview

**Request:**

```bash
curl -X POST http://localhost:5000/interviews \
  -H "Content-Type: application/json" \
  -d '{
    "interviewee_name": "John Doe",
    "interviewer_name": "Jane Smith",
    "interview_datetime": "2023-12-31T14:30:00.000",
    "interview_duration_min": 60,
    "status": "SCHEDULED"
  }'
```

**Response:**

```bash
{
  "message": "Interview created successfully"
}
```

### 2. Retrieve Details of an Interview

**Request:**

```bash
curl http://localhost:5000/interviews/1
```

**Response:**
```bash
{
  "id": 1,
  "interviewee_name": "John Doe",
  "interviewer_name": "Jane Smith",
  "interview_datetime": "2023-12-31T14:30:00.000",
  "interview_duration_min": 60,
  "status": "SCHEDULED",
  "created_at": "2023-12-23T12:00:00.000",
  "updated_at": "2023-12-23T12:30:00.000"
}
```

### 3. Update an Existing Interview

**Request:**

```bash
curl -X PATCH http://localhost:5000/interviews/1 \
  -H "Content-Type: application/json" \
  -d '{
    "interview_duration_min": 60,
    "status": "CANCELED"
  }'
```

**Response:**
```bash
{
  "message": "Interview updated successfully"
}
```

### 4. Delete an Interview

**Request:**

```bash
curl -X DELETE http://localhost:5000/interviews/1
```

**Response:**
```bash
{
  "message": "Interview deleted successfully"
}
```

### 5. List All Interviews

**Request:**

```bash
curl http://localhost:5000/interviews
```

**Response:**
```bash
[
  {
    "interviewee_name": "John Doe",
    "interviewer_name": "Jane Smith",
    "interview_datetime": "2023-12-31T14:30:00.000",
    "interview_duration_min": 75,
    "status": "ONGOING",
    "created_at": "2023-12-23T12:00:00.000",
    "updated_at": "2023-12-23T12:45:00.000"
  },
  ...
]
```
