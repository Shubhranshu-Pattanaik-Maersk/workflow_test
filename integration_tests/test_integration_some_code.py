# integration_tests/test_integration_some_code.py

import unittest
import psycopg2

class TestIntegrationWithDatabase(unittest.TestCase):
    
    def setUp(self):
        self.connection = psycopg2.connect(
            dbname="test_db",
            user="postgres",
            password="postgres",
            host="postgres",  # Use the service name as the host
            port="5432"
        )
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def test_database_insertion(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id serial PRIMARY KEY, name VARCHAR(50));")
        self.cursor.execute("INSERT INTO test_table (name) VALUES ('Test Name');")
        self.connection.commit()

        self.cursor.execute("SELECT * FROM test_table WHERE name = 'Test Name';")
        result = self.cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'Test Name')

if __name__ == '__main__':
    unittest.main()
