"""
Example usage of the DatabaseConnection singleton class
"""
from connection import DatabaseConnection


def get_all_roles():
    """Example function to get all roles"""
    db = DatabaseConnection()
    try:
        results = db.execute_query("SELECT * FROM RoleView")
        return results
    except Exception as e:
        print(f"Error fetching roles: {e}")
        return []


def get_role_by_id(role_id: int):
    """Example function to get role by ID with parameters"""
    db = DatabaseConnection()
    try:
        query = "SELECT * FROM RoleView WHERE Id = ?"
        results = db.execute_query(query, (role_id,))
        return results[0] if results else None
    except Exception as e:
        print(f"Error fetching role by ID: {e}")
        return None


def insert_example_data(table_name: str, name: str):
    """Example function for INSERT operation"""
    db = DatabaseConnection()
    try:
        query = f"INSERT INTO {table_name} (Name) VALUES (?)"
        affected_rows = db.execute_non_query(query, (name,))
        print(f"Inserted {affected_rows} row(s)")
        return affected_rows
    except Exception as e:
        print(f"Error inserting data: {e}")
        return 0


def main():
    """Main function demonstrating usage"""
    
    # All these calls will use the same database connection instance
    print("=== Getting all roles ===")
    roles = get_all_roles()
    for role in roles:
        print(role)
    
    print("\n=== Getting role by ID ===")
    role = get_role_by_id(1)
    if role:
        print(role)
    else:
        print("Role not found")
    
    # Example of multiple instances - they're the same object
    print("\n=== Singleton test ===")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"Same instance: {db1 is db2}")  # Should print True
    
    # Close connection when application ends
    db1.close_connection()


if __name__ == "__main__":
    main()