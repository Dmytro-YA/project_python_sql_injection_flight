# Flight Management System (SQL Injection Demo)

A simple Python application to manage flight data using an SQLite database. This project demonstrates basic database operations (CRUD) and illustrates common SQL injection vulnerabilities for educational purposes.

## Overview

The application allows users to interact with a flight database through a command-line interface. It includes features for:
- Listing all flights.
- Adding new flights.
- Searching for flights by number or parameters (departure/destination).
- Deleting flights.
- Demonstrating SQL injection vulnerabilities via specific search fields.

## Requirements

- **Python 3.x**
- **SQLite3** (typically bundled with Python)
- No external dependencies are required.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd project_python_sql_injection_flight
    ```

2.  **Initialize the Database:**
    The database (`flight.db`) is automatically created when you run the application for the first time.

## Usage

Run the main application using the following command:

```bash
python3 Flight_class.py
```

### Menu Options:
1.  **Show Flights**: Displays all records in the `flight` table.
2.  **Add Flight**: Prompts for details to insert a new flight record.
3.  **Show flight by number**: Search for a flight using its numeric ID.
4.  **Delete flight**: Prompts for a flight number to remove from the database.
5.  **Show flight by parametr**: Search for flights by departure and destination cities.
6.  **EXIT**: Closes the application.
7.  **SQL injection**: A specific entry point to test SQL injection payloads.

## Flask Web Application

A new Flask web interface has been added to provide a graphical way to interact with the flight database.

### Requirements:
- **Flask** (Install via `pip install Flask`)

### Running the Flask App:
1.  **Install dependencies:**
    ```bash
    pip install Flask
    ```
2.  **Run the application:**
    ```bash
    python3 app.py
    ```
3.  **Access the interface:**
    Open your browser and navigate to `http://127.0.0.1:5001`.

### Features:
- **Home**: View all flights in a table.
- **Add Flight**: Web form to add new flights.
- **Search**: Search for flights by number, parameters, or test SQL injection payloads via the web interface.
- **Delete**: Remove flights directly from the list.

## SQL Injection Demonstration

The `sql_injection` method (Option 7) and `show_flight_by_parametr` (Option 5) demonstrate how unsanitized user input can be exploited.

**Example Payload (Option 7):**
When prompted for a flight number, entering `' OR '1'='1` might return all flights instead of a specific one, illustrating how the query logic can be bypassed.

## Running Tests

Unit tests are provided using Python's built-in `unittest` framework.

To run the tests:
```bash
python3 -m unittest test_Flight_class.py
```

## Project Structure

- `Flight_class.py`: Main application logic and database interactions.
- `test_Flight_class.py`: Unit tests for the `Flight` class.
- `flight.db`: SQLite database file (generated at runtime).
- `README.md`: Project documentation.

## Environment Variables

No environment variables are currently used by this project.

## Scripts

- **Entry Point**: `Flight_class.py` contains the `main()` loop.
- **Test Script**: `test_Flight_class.py` for automated verification.

## License

TODO: Add license information.
