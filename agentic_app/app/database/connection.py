import os
from dotenv import load_dotenv
import pyodbc
import threading
from typing import Optional

load_dotenv()


class DatabaseConnection:
    """Singleton database connection class for SQL Server"""
    
    _instance: Optional['DatabaseConnection'] = None
    _lock = threading.Lock()
    _connection: Optional[pyodbc.Connection] = None
    
    def __new__(cls) -> 'DatabaseConnection':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._connection_string = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                f"SERVER={os.getenv('DB_SERVER')};"
                f"DATABASE={os.getenv('DB_NAME')};"
                f"UID={os.getenv('DB_USER_NAME')};"
                f"PWD={os.getenv('DB_PASSWORD')};"
            )
    
    def get_connection(self) -> pyodbc.Connection:
        """Get database connection, create if doesn't exist"""
        if self._connection is None or self._connection.closed:
            try:
                self._connection = pyodbc.connect(self._connection_string)
                print("Database connection established successfully")
            except pyodbc.Error as e:
                print(f"Error connecting to database: {e}")
                raise
        return self._connection
    
    def get_cursor(self) -> pyodbc.Cursor:
        """Get a cursor from the connection"""
        return self.get_connection().cursor()
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """Execute a SELECT query and return results"""
        cursor = self.get_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            cursor.close()
    
    def execute_non_query(self, query: str, params: tuple = None) -> int:
        """Execute INSERT, UPDATE, DELETE queries and return affected rows"""
        cursor = self.get_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            affected_rows = cursor.rowcount
            self._connection.commit()
            return affected_rows
        except pyodbc.Error as e:
            self._connection.rollback()
            print(f"Error executing non-query: {e}")
            raise
        finally:
            cursor.close()
    
    def close_connection(self):
        """Close the database connection"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            print("Database connection closed")
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        if hasattr(self, '_connection'):
            self.close_connection()

