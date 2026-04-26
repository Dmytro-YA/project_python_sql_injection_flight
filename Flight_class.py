import sqlite3
from werkzeug.security import check_password_hash



class Flight:
    def __init__(self):
        self.db_path = 'flight.db'
        self.create_flight_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_flight_table(self):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                'CREATE TABLE IF NOT EXISTS flight('
                'id INTEGER PRIMARY KEY, number TEXT, departure TEXT, destination TEXT, capacity INTEGER, '
                'number_of_passengers INTEGER, status TEXT, time_to_flight INTEGER)')
            cur.execute(
                'CREATE TABLE IF NOT EXISTS users('
                'id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
            cur.execute(
                'CREATE TABLE IF NOT EXISTS bookings('
                'id INTEGER PRIMARY KEY, user_id INTEGER, flight_number TEXT, seats INTEGER, '
                'FOREIGN KEY(user_id) REFERENCES users(id), '
                'FOREIGN KEY(flight_number) REFERENCES flight(number))')

    def register_user(self, username, password):
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        with self._get_connection() as conn:
            cur = conn.cursor()
            # 1. Ищем пользователя ТОЛЬКО по имени
            cur.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cur.fetchone()

            # Если пользователь найден
            if user:
                # Предположим, что хеш пароля находится в колонке под индексом 2
                # user[0] - id, user[1] - username, user[2] - password (hash)
                stored_hash = user[2]

                # 2. Проверяем, совпадает ли введенный пароль с хешем из БД
                if check_password_hash(stored_hash, password):
                    return user  # Возвращаем кортеж с данными пользователя

            # Если пользователь не найден или пароль не подошел
            return None

    def add_flight(self, number=0, departure='None', destination='None',
                   capacity=0, number_of_passengers=0, status='None', time_to_flight=0):
        """Add a new flight to the 'flight' table."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO flight (number, departure, destination, capacity, number_of_passengers, '
                             'status, time_to_flight) VALUES (?, ?, ?, ?, ?, ?, ?)', (number, departure, destination,
                                                                                      capacity, number_of_passengers,
                                                                                      status, time_to_flight))
            conn.commit()

    def show_flight(self):
        """Display all flights in the 'flight' table."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT number, departure, destination, capacity, '
                             'number_of_passengers, status, time_to_flight, (capacity - number_of_passengers) AS available_seats FROM flight')
            flight = cur.fetchall()
        return flight

    def show_flight_by_number(self, num):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT number, departure, destination, capacity, "
                        "number_of_passengers, status, time_to_flight, (capacity - number_of_passengers) AS available_seats "
                        "FROM flight WHERE number = ?", (num,))
            number_flight = cur.fetchall()
        return number_flight

    def delete_flight(self, num):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM bookings WHERE flight_number = ?", (num,))
            cur.execute("DELETE FROM flight WHERE number = ?", (num,))
            conn.commit()

    def show_flight_by_parametr(self, departure_name, destination_name):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT number, departure, destination, capacity, "
                "number_of_passengers, status, time_to_flight, (capacity - number_of_passengers) AS available_seats "
                "FROM flight WHERE departure = ? AND destination = ?", (departure_name, destination_name))
            number_flight = cur.fetchall()
        return number_flight

    def book_flight(self, num, user_id, seats=1):
        """Decrease available seats by increasing the number of passengers and record the booking."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            # First, check if there's enough capacity
            cur.execute("SELECT capacity, number_of_passengers FROM flight WHERE number = ?", (num,))
            flight = cur.fetchone()
            
            if flight:
                capacity, passengers = flight
                if passengers + seats <= capacity:
                    cur.execute("UPDATE flight SET number_of_passengers = number_of_passengers + ? WHERE number = ?", (seats, num))
                    cur.execute("INSERT INTO bookings (user_id, flight_number, seats) VALUES (?, ?, ?)", (user_id, num, seats))
                    conn.commit()
                    return True, f"{seats} seats booked successfully!"
                else:
                    available = capacity - passengers
                    return False, f"Not enough available seats on this flight. Only {available} remaining."
            else:
                return False, "Flight not found."

    def get_user_bookings(self, user_id):
        """Retrieve all bookings for a specific user with flight details."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT b.flight_number, f.departure, f.destination, b.seats, f.status, f.time_to_flight "
                "FROM bookings b "
                "JOIN flight f ON b.flight_number = f.number "
                "WHERE b.user_id = ?", (user_id,))
            bookings = cur.fetchall()
        return bookings

    def sql_injection(self, flight_number):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT number, departure, destination, capacity, "
                        f"number_of_passengers, status, time_to_flight, (capacity - number_of_passengers) AS available_seats "
                        f"FROM flight WHERE number = '{flight_number}'")
            flight_number = cur.fetchall()
        return flight_number


def main():
    app = Flight()

    while True:
        print("\nFlight Menu:")
        print("1. Show all flights")
        print("2. Add flight")
        print("3. Show flight by number")
        print("4. Delete flight")
        print("5. Show flight by parameter")
        print("6. EXIT")
        print("7. SQL injection")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            flights = app.show_flight()
            if flights:
                for f in flights:
                    print(f)
            else:
                print('No flights found.')
        elif choice == '2':
            new_flight = input('Enter a flight number: ')
            new_departure = input('Enter a departure city: ')
            new_destination = input('Enter a destination city: ')
            new_capacity = int(input('Enter a capacity(number): '))
            new_number_of_passengers = int(input('Enter a number of passengers(number): '))
            new_status = input('Enter a status: ')
            new_time_to_flight = float(input('Enter a time to flight(number): '))
            app.add_flight(new_flight, new_departure, new_destination, new_capacity,
                           new_number_of_passengers, new_status, new_time_to_flight)
            print("Flight added successfully!")
        elif choice == '3':
            num = input('Enter number of flight: --->>>')
            flights = app.show_flight_by_number(num)
            if flights:
                for f in flights:
                    print(f)
            else:
                print('No flight with this number')

        elif choice == '4':
            num = int(input('Enter number of flight to delete: --->>>'))
            app.delete_flight(num)
            print(f'{num} flight was deleted successful!')

        elif choice == '5':
            departure_name = input('Enter departure: --->>>')
            destination_name = input('Enter destination: --->>>')
            flights = app.show_flight_by_parametr(departure_name, destination_name)
            if flights:
                for f in flights:
                    print(f)
            else:
                print('No flight with this parameters')

        elif choice == '6':
            print("Exiting the program.")
            break

        elif choice == '7':
            flight_number = input('Enter flight number: ')
            flights = app.sql_injection(flight_number)
            if flights:
                for f in flights:
                    print(f)
            else:
                print('No flight with this parameters')
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
# # задержка рейса
# def delay_flight(self):
# self.delayed = True
#
# # убрать задержку
# def clear_delay(self):
# self.delayed = False
#
# # изменить время полета
# def change_duration(self, new_time):
# self.duration = new_time
#
# # проверка переполнения
# def is_full(self):
# return self.occupied >= self.capacity
#
# # проверка почти полного самолета
# def almost_full(self):
# return self.occupancy_rate() > 90
#
# # изменение маршрута
# def change_destination(self, new_destination):
# self.destination = new_destination
# свободные места
# def free_seats(self):
# return self.capacity - self.occupied
#
# # процент заполненности
# def occupancy_rate(self):
# return (self.occupied / self.capacity) * 100
#
# # посадка пассажира
# def add_passenger(self, number=1):
# if self.occupied + number <= self.capacity:
# self.occupied += number
# print("Пассажиры добавлены")
# else:
# print("Нет свободных мест")
#
# # высадка пассажира
# def remove_passenger(self, number=1):
# if self.occupied - number >= 0:
# self.occupied -= number
# print("Пассажиры вышли")
# else:
# print("Ошибка количества")
