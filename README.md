# ISPH Stock Exchange Backend

A backend application for a stock exchange simulation, created using Flask, Flask-RESTful, and JSON data storage. This application allows students to simulate stock trading based on classroom achievements, with real-time price adjustments, point tracking, and a leaderboard.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/ISPH-Stock-Exchange.git
```

### 2. Set Up a Virtual Environment

It's recommended to set up a virtual environment to manage dependencies:

```bash
python3.12 -m venv venv  # Or use python3.10 / python3.11 if you prefer
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

After activating the virtual environment, install the required packages:

```bash
pip install flask==2.1.3 werkzeug==2.0.3 flask-restful flask-restx
```

### 4. Load the JSON Data

Make sure you have the following JSON files in your project directory:

- `users.json`: Stores user data (e.g., students and teachers).
- `portfolios.json`: Stores user portfolios, including stock holdings and points balance.
- `houses.json`: Stores house data, including stock prices and price history.

If these files are not available, you can create sample files or use your own data structure.

## Setup

### 1. Configure Flask

The Flask app is ready to run once the dependencies are installed. The main script for running the app is `dummy.py`. This file includes the setup for Flask, Flask-RESTful API routes, and the JSON data loading function.

### 2. Run the Application

Start the Flask development server:

```bash
python dummy.py
```

By default, the application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## API Endpoints

### 1. `POST /register`

- **Description**: Register a new user with a house assignment.
- **Request Body**:
  ```json
  {
    "username": "student_name",
    "house": "Rua_Bien"
  }
  ```
- **Response**:
  ```json
  {
    "message": "This endpoint is for demonstration only."
  }
  ```

### 2. `GET /houses`

- **Description**: Fetch the list of houses and current stock values.
- **Response**:
  ```json
  {
    "houses": {
      "Rua_Bien": { "current_price": 100, "volume": 5000 },
      "Voi": { "current_price": 120, "volume": 4000 },
      "Te_Giac": { "current_price": 90, "volume": 3000 },
      "Ho": { "current_price": 110, "volume": 6000 }
    }
  }
  ```

### 3. `POST /buy`

- **Description**: Handle buying stocks for a specific house.
- **Request Body**:
  ```json
  {
    "username": "student_name",
    "house": "Rua_Bien",
    "amount": 100
  }
  ```
- **Response**:
  ```json
  {
    "message": "This endpoint is for demonstration only."
  }
  ```

### 4. `POST /sell`

- **Description**: Handle selling stocks for a specific house.
- **Request Body**:
  ```json
  {
    "username": "student_name",
    "house": "Rua_Bien",
    "amount": 50
  }
  ```
- **Response**:
  ```json
  {
    "message": "This endpoint is for demonstration only."
  }
  ```

### 5. `GET /portfolio`

- **Description**: View a student’s current stock portfolio and points balance.
- **Query Parameters**: `username`
- **Response**:
  ```json
  {
    "portfolio": {
      "Rua_Bien": 100,
      "Voi": 50
    },
    "points_balance": 200
  }
  ```

### 6. `POST /earn-points`

- **Description**: Update student points based on good performance.
- **Request Body**:
  ```json
  {
    "username": "student_name",
    "points": 10
  }
  ```
- **Response**:
  ```json
  {
    "message": "This endpoint is for demonstration only."
  }
  ```

### 7. `GET /leaderboard`

- **Description**: Display the top students or houses based on stock performance and points.
- **Response**:
  ```json
  {
    "leaderboard": [
      { "username": "student_name", "points_balance": 200 },
      { "username": "another_student", "points_balance": 150 }
    ]
  }
  ```

### 8. `GET /price-history/<house_name>`

- **Description**: View the price history for a specific house.
- **Response**:
  ```json
  {
    "price_history": [
      { "date": "2024-11-01", "price": 100 },
      { "date": "2024-11-02", "price": 105 }
    ]
  }
  ```

### 9. `GET /all-houses`

- **Description**: Fetch data for all houses.
- **Response**:
  ```json
  {
    "houses": [
      { "name": "Rua_Bien", "current_price": 100, "volume": 5000 },
      { "name": "Voi", "current_price": 120, "volume": 4000 }
    ]
  }
  ```
