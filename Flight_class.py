import sqlite3


class Flight:
    def __init__(self):
        self.conn = sqlite3.connect('flight.db')
        self.cur = self.conn.cursor()
        self.create_flight_table()

    def create_flight_table(self):
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS flight('
            'id INTEGER PRIMARY KEY, number INTEGER, departure TEXT, destination TEXT, capacity INTEGER, '
            'number_of_passengers INTEGER, status TEXT, time_to_flight INTEGER)')

    def add_flight(self, number=0, departure='None', destination='None',
                   capacity=0, number_of_passengers=0, status='None', time_to_flight=0):
        """Add a new flight to the 'flight' table."""
        self.cur.execute('INSERT INTO flight (number, departure, destination, capacity, number_of_passengers, '
                         'status, time_to_flight) VALUES (?, ?, ?, ?, ?, ?, ?)', (number, departure, destination,
                                                                                  capacity, number_of_passengers,
                                                                                  status, time_to_flight))
        self.conn.commit()

    def show_flight(self):
        """Display all flights in the 'flight' table."""
        self.cur.execute('SELECT number, departure, destination, capacity, '
                         'number_of_passengers, status, time_to_flight FROM flight')
        flight = self.cur.fetchall()
        # print(flight)
        if flight:
            for f in flight:
                print(f)
        else:
            print('No flights found.')

    def show_flight_by_number(self, num):
        self.cur.execute(f'SELECT * FROM flight WHERE number = {num}')
        number_flight = self.cur.fetchall()
        # print(number_flight)
        if number_flight:
            for n in number_flight:
                print(n)
        else:
            print('No flight with this number')

    def delete_flight(self):
        num = int(input('Enter number of flight to delete: --->>>'))

        self.cur.execute(f'DELETE FROM flight WHERE number = {num}')
        print(f'{num} flight was deleted successful!')

        self.conn.commit()

    def show_flight_by_parametr(self):
        departure_name = input('Enter departure: --->>>')
        destination_name = input('Enter destination: --->>>')

        self.cur.execute(
            f"SELECT * FROM flight WHERE departure = '{departure_name}' AND destination = '{destination_name}'")
        number_flight = self.cur.fetchall()
        # print(number_flight)
        if number_flight:
            for n in number_flight:
                print(n)
        else:
            print('No flight with this parameters')

    def sql_injection(self):
        flight_number = input('Enter flight number: ')
        self.cur.execute(f"SELECT * FROM flight WHERE number = '{flight_number}'")
        flight_number = self.cur.fetchall()
        if flight_number:
            for n in flight_number:
                print(n)
        else:
            print('No flight with this parameters')


def main():
    app = Flight()

    while True:
        print("\nFlight Menu:")
        print("1. Show Flights")
        print("2. Add Flight")
        print("3. Show flight by number")
        print("4. Delete flight")
        print("5. Show flight by parametr")
        print("6. EXIT")
        print("7. SQL injection")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            app.show_flight()
        elif choice == '2':
            new_flight = int(input('Enter a flight number(number): '))
            new_departure = input('Enter a departure city: ')
            new_destination = input('Enter a destination city: ')
            new_capacity = int(input('Enter a capacity(number): '))
            new_number_of_passengers = int(input('Enter a number of passengers(number): '))
            new_status = input('Enter a status: ')
            new_time_to_flight = float(input('Enter a time to flight(number): '))
            app.add_flight(new_flight, new_departure, new_destination, new_capacity,
                           new_number_of_passengers, new_status, new_time_to_flight)
        elif choice == '3':
            num = int(input('Enter number of flight: --->>>'))
            app.show_flight_by_number(num)

        elif choice == '4':
            # num = int(input('Enter number of flight to delete: --->>>'))
            app.delete_flight()

        elif choice == '5':
            app.show_flight_by_parametr()

        elif choice == '6':
            print("Exiting the program.")
            break

        elif choice == '7':
            app.sql_injection()
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
