from typing import Any, Dict, List
from files_handler.file_loader import FileLoader
from database.connection import DatabaseConnection
from database.query_helper import QueryHelper


class RoleRepository:
    
    def __init__(self):
        self.db = DatabaseConnection()

    def get_roles(self) -> List[Dict[str, Any]]:
        """Get all roles from the RoleView table
        
        Returns:
            List[Dict[str, Any]]: List of role dictionaries with OwnerId, RoleId, Name
        """
        try:
            # Use direct query since QueryHelper might not be available
            roles_data = self.db.execute_query(QueryHelper.GetRoles)
            
            # Convert tuples to dictionaries for better handling
            roles = []
            for role in roles_data:
                # Column names: OwnerId, RoleId, Name
                role_dict = {
                    'OwnerId': role.OwnerID,
                    'RoleId': role.RoleID,
                    'Name': role.Name
                }
                roles.append(role_dict)
            
            print(f"Successfully fetched {len(roles)} roles")
            return roles
            
        except Exception as e:
                print(f"Error fetching roles: {e}")
                return []
