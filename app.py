"""Main application module for the flight booking system."""
import re
import secrets

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from Flight_class import Flight

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
flight_model = Flight()

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/flights', methods=['GET', 'POST'])
def flights():
    """Display all flights. Accessible only to logged-in users."""
    # Only logged in users can see flights
    if 'user_id' not in session:
        return redirect(url_for('login'))
    all_flights = flight_model.show_flight()
    return render_template('flights.html', flights=all_flights)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        hash_password = generate_password_hash(password)
        unhashed_password = check_password_hash(hash_password, password)
        print(username, password, confirm_password, hash_password, unhashed_password)

        error = validate_registration(username, password, confirm_password)
        if not error:
            if flight_model.register_user(username, hash_password):
                return redirect(url_for('login'))
            error = "Email already exists."
    return render_template('register.html', error=error)

def validate_registration(username, password, confirm_password):
    """Validate user registration details."""
    if not username or not password:
        return "Email and password are required."

    # Email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, username):
        return "Please enter a valid email address."

    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if len(password) > 15:
        return "Password must be less than 16 characters long."

    if password != confirm_password:
        return "Passwords do not match."
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = flight_model.login_user(username, password)

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        error = "Invalid email or password."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """Log out the current user."""
    session.clear()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_flight():
    """Add a new flight. Accessible only to logged-in users."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST':
        number = request.form.get('number')
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        try:
            capacity = int(request.form.get('capacity', 0))
            passengers = int(request.form.get('passengers', 0))
            time_to_flight = float(request.form.get('time_to_flight', 0))
            status = request.form.get('status')

            flight_model.add_flight(
                number, departure, destination, capacity, passengers, status, time_to_flight
            )
            return redirect(url_for('flights'))
        except ValueError:
            error = "Invalid input for Capacity, Passengers, or Time. Please enter numbers."

    return render_template('add_flight.html', error=error)

@app.route('/delete/<number>', methods=['POST'])
def delete_flight(number):
    """Delete a flight. Accessible only to logged-in users after password verification."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    password = request.form.get('password')
    username = session.get('username')
    # Verify password using the existing login_user method
    user = flight_model.login_user(username, password)

    if user:
        flight_model.delete_flight(number)
        flash(f'Flight {number} and all its bookings have been deleted.', 'success')
    else:
        flash('Invalid password. Flight deletion failed.', 'danger')

    return redirect(url_for('flights'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search for flights by number or parameters."""
    results = None
    if request.method == 'POST':
        search_type = request.form.get('search_type')
        if search_type == 'number':
            number = request.form.get('number')
            results = flight_model.show_flight_by_number(number)
        elif search_type == 'params':
            departure = request.form.get('departure')
            destination = request.form.get('destination')
            results = flight_model.show_flight_by_parametr(departure, destination)
        elif search_type == 'sql':
            number = request.form.get('number')
            results = flight_model.sql_injection(number)
    return render_template('search.html', results=results)

@app.route('/book', methods=['GET', 'POST'])
def book():
    """Handle flight search and booking."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    results = None
    message = None
    message_type = None

    if request.method == 'POST':
        action = request.form.get('action')
        results, message, message_type = handle_post_book(action)
    else:
        results, message, message_type = handle_get_book()

    return render_template('book.html', results=results, message=message, message_type=message_type)

def handle_post_book(action):
    """Handle POST requests for the booking route."""
    results, message, message_type = None, None, None
    if action == 'search':
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        results = flight_model.show_flight_by_parametr(departure, destination)
        if not results:
            message = "No flights found matching your route."
            message_type = "info"
    elif action == 'book':
        number = request.form.get('number')
        try:
            num_seats = int(request.form.get('num_seats', 1))
            if num_seats < 1:
                message = "Number of seats must be at least 1."
                message_type = "danger"
            else:
                success, msg = flight_model.book_flight(number, session['user_id'], num_seats)
                message = msg
                message_type = "success" if success else "danger"
        except ValueError:
            message = "Invalid input for number of seats."
            message_type = "danger"
    return results, message, message_type

def handle_get_book():
    """Handle GET requests for the booking route."""
    results, message, message_type = None, None, None
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    number = request.args.get('number')

    if departure and destination:
        results = flight_model.show_flight_by_parametr(departure, destination)
    elif number:
        flight = flight_model.show_flight_by_number(number)
        if flight:
            results = flight
        else:
            message = f"Flight {number} not found."
            message_type = "info"
    return results, message, message_type

@app.route('/account')
def account():
    """Display the user's account and bookings."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_bookings = flight_model.get_user_bookings(session['user_id'])
    return render_template('account.html', bookings=user_bookings)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5001)
