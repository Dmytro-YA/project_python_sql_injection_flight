from unittest import TestCase
import os
import sqlite3

from Flight_class import Flight


class TestFlight(TestCase):
    def test_create_flight_table(self):
        """
        delete file database before testing if file exist
        """
        if os.path.exists("flight.db"):
            os.remove("flight.db")

        """
        create object flight
        
        """
        from Flight_class import Flight
        flight = Flight()
        """
        check if table created
        """

        cursor = flight._get_connection().cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flight'")
        table_exist = cursor.fetchone()[0]
        print(table_exist)
        self.assertEqual(table_exist, "flight")



