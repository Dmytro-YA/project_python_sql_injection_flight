# Flight Management System (SQL Injection Demo)

A simple Python application to manage flight data using an SQLite database. This project demonstrates basic database operations (CRUD), user authentication, and illustrates common SQL injection vulnerabilities for educational purposes.

## Overview

The application allows users to interact with a flight database through both a Command-Line Interface (CLI) and a modern Flask Web Interface.

### Core Features:
- **User Authentication**: Secure registration and login system with password hashing.
- **Flight Management**: List, add, search, and delete flights.
- **Booking System**: Users can book flights and view their bookings in their account profile.
- **SQL Injection Demo**: Dedicated entry points to test and understand SQL injection vulnerabilities.

## Requirements

- **Python 3.x**
- **SQLite3** (typically bundled with Python)
- **Flask** (for the web interface)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:Dmytro-YA/project_python_sql_injection_flight.git
    cd project_python_sql_injection_flight
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the Database:**
    The database (`flight.db`) is automatically created when you run the application for the first time.

## Usage

### 1. Command-Line Interface (CLI)
Run the CLI application:
```bash
python3 Flight_class.py
```
**Menu Options:**
- **Show Flights**: Displays all records.
- **Add Flight**: Insert a new flight record.
- **Show flight by number**: Search by numeric ID.
- **Delete flight**: Remove a flight by number.
- **Show flight by parametr**: Search by departure and destination.
- **SQL injection**: Entry point for testing injection payloads.

### 2. Flask Web Application
Run the web interface:
```bash
python3 app.py
```
Access the interface at `http://127.0.0.1:5000` (or the port specified in the console).

**Web Features:**
- **Registration/Login**: Create an account to access management features.
- **Dashboard**: View and manage all available flights.
- **Booking**: Book seats on flights and manage them in your profile.
- **Search**: Advanced search including SQL injection testing fields.

## SQL Injection Demonstration

The `sql_injection` methods demonstrate how unsanitized user input can be exploited.

**Example Payload:**
When prompted for a flight number, entering `' OR '1'='1` might return all flights instead of a specific one, illustrating how the query logic can be bypassed.

## Quality Assurance & Testing

This project includes a comprehensive testing suite and documentation.

### Running Tests:
- **Unit Tests**: `python3 -m unittest test_Flight_class.py`
- **Extended Tests**: `python3 -m unittest test_Flight_class_extended.py`
- **UI Tests**: `python3 -m unittest test_ui.py`

### Testing Documentation:
The `testing/` directory contains detailed QA artifacts:
- **Test Plan & Scenarios**: Structured approach to verifying the application.
- **Bug Reports**: Documented vulnerabilities and functional issues.
- **Test Cases**: Specific steps to verify each feature (Add, Delete, Search, SQLi).

## Project Structure

- `Flight_class.py`: Core logic and database interactions (CLI entry point).
- `app.py`: Flask web application and routing.
- `templates/`: HTML templates for the web interface.
- `testing/`: Comprehensive test documentation and bug reports.
- `test_*.py`: Automated test scripts (Unit, Extended, UI).
- `flight.db`: SQLite database.
- `report.gif` / `search_report.gif`: Visual demonstrations of the system.

## License

TODO: Add license information.
