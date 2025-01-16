# nava2105/Personal-Data-Storage

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-%23000000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

---

## Table of Contents
1. [General Info](#general-info)
2. [Features](#features)
3. [Technologies](#technologies)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Database Schema](#database-schema)

---

## General Info

This project is a backend API for managing and storing user personal data securely. It integrates a Flask-based REST API with MySQL as the database. The API interacts with an external authentication service via JWT for user validation and authorization.

---

## Features

### Key Features:
- **User Management**
  - Retrieve details of registered users, including their personal data like age, height, weight, and body structure.
  - Securely map user data to unique users with a `user_id` fetched via external API.

- **Authentication & Authorization**
  - Authorization is handled by communicating with an external service over HTTP using **JWT tokens**.
  - Ensures only registered users can access and store personal data.

- **Abstract Factory Pattern**
  - Designed with a factory-based architecture for flexible database implementations (MySQL, other DBs in the future).

---

## Technologies

- [Python](https://www.python.org/): Version 3.9
- [Flask](https://flask.palletsprojects.com/): For creating REST APIs
- [SQLAlchemy](https://www.sqlalchemy.org/): Object-relational mapper for database interactions
- [MySQL](https://www.mysql.com/): Relational database management
- [PyMySQL](https://github.com/PyMySQL/PyMySQL): Database adapter for Python

---

## Installation

### Prerequisites:
1. **Python 3.9**: Install Python and ensure it is added to the PATH.
2. **MySQL**: Ensure MySQL is installed and running.
3. **Environment Setup**:
   - Clone this repository:
     ```bash
     git clone https://github.com/nava2105/Personal-Data-Storage.git
     cd Personal-Data-Storage
     ```

   - Create and activate a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate    # Linux/MacOS
     venv\Scripts\activate       # Windows
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables** in `.env` (modify as per your MySQL setup):
   ```plaintext
   AUTH_URL="nava2105/Spring-Security-JWT api url"
   DB_NAME="your_database_name"
   DB_USER="your_mysql_username"
   DB_PASSWORD="your_mysql_password"
   DB_IP="localhost"
   DB_PORT="3306 or 3307"
   ```

6. **Create the database structure**:
   ```bash
   flask db upgrade
   ```
   
7. Start the Flask development server:
   ```bash
   python app.py
   ```

8. Access the API at `http://localhost:5000`.

---

## Usage

Once the application is up and running, you can interact with the API by performing proper requests:

### Register Personal Data:
- Endpoint: `/register/personal/data`
- Headers:
  ```
  Authorization: Bearer your_jwt_token
  ```
- Payload:
  ```json
  {
    "birth_date": "user's birth date YYYY-MM-DD",
    "height": "user's height",
    "weight": "user's weight",
    "body_structure": "user's body structure"
  }
  ```

### Modify Personal Data:
- Endpoint: `/modify/personal/data`
- Headers:
  ```
  Authorization: Bearer your_jwt_token
  ```
- Payload:
  ```json
  {
    "birth_date": "user's birth date YYYY-MM-DD",
    "height": "user's height",
    "weight": "user's weight",
    "body_structure": "user's body structure"
  }
  ```

### Get Personal Data:
- Endpoint: `/get/personal/data`
- Headers:
  ```
  Authorization: Bearer your_jwt_token
  ```
- Payload:
  ```json
  {}
  ```
  
---

## Endpoints
Below is a comprehensive list of the endpoints included in the project:

### Protected Endpoints (Authentication Required)
- **Register Personal Data**
  - `POST /register/personal/data`
  - Allows users to register their personal data, their user code is retrieved from the auth api.
  - Requires the JWT.

- **Modify Personal Data**
  - `POST /modify/personal/data`
  - Allows users to modify their personal data, their user code is retrieved from the auth api.
  - Requires the JWT.

- **Get Personal Data**
  - `GET /get/personal/data`
  - Allows users to consult their personal data, their user code is retrieved from the auth api.
  - Requires the JWT.

---

## Database Schema

Below is the database schema used in this project:

### Tables:

#### `user` Table:
| **Column**  | **Type**       | **Description**          |
|-------------|----------------|--------------------------|
| `user_id`   | BigInteger     | Primary Key              |
| `user_name` | String         | Unique username          |
| `password`  | String         | Hashed password          |

#### `personal_data` Table:
| **Column**         | **Type**   | **Description**                                                 |
|--------------------|------------|-----------------------------------------------------------------|
| `personal_data_id` | BigInteger | Primary Key                                                     |
| `user_id`          | BigInteger | Foreign Key referencing `user.user_id`                          |
| `age`              | Integer    | Age of the user                                                 |
| `height`           | Double     | Height of the user (in meters)                                  |
| `weight`           | Double     | Weight of the user (in kilograms)                               |
| `body_structure`   | String     | Description of the user's body structure (e.g., Lean, Athletic) |

---

## Notes:

1. **Authentication**:
   - JWT token management is handled via an external endpoint (`${AUTH_URL}`), ensuring API is decoupled from authentication logic.

2. **Database Configurations**:
   - All database configurations are loaded from environment variables in `.env`.

3. **Factory-Based Design**:
   - The architecture incorporates the **Abstract Factory Pattern** to enable seamless switching of database implementations without major overhauls.

--- 
