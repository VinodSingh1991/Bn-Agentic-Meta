
from typing import Any, Dict, List
from utils.layout_helper import LayoutHelper
from database.connection import DatabaseConnection
from database.query_helper import QueryHelper
from enum_helper.field_type import field_type_inverted
from enum_helper.object_list import object_list
from files_handler.file_loader import FileLoader

class ListingRepository:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.loader = FileLoader()
        self.layout_helper = LayoutHelper()
        
    def get_object_enum_by_object_id(self, object_id: int) -> str:
        """Get the object name from the object_list enum by object ID"""

        return object_list.get(object_id, "UnknownObject")


    def get_rpt_listing(self) -> List[Dict[str, Any]]:
        """Get all fields from the Rpt_query table

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            # Use direct query since QueryHelper might not be available
            listing_data = self.db.execute_query(QueryHelper.GetListingFromRptQuery)

            # Convert tuples to dictionaries for better handling
            listing = []
            for obj in listing_data:
                # Column names: OwnerId, RoleId, Name
                object_name = self.get_object_enum_by_object_id(obj.KeyId)

                if object_name == "UnknownObject":
                    continue

                columns = self.layout_helper.get_field_from_xml_query_info(obj.SourceExpression)
                obj_dict = {
                    "ObjectId": obj.KeyId,
                    "ObjectName": object_name,
                    "ReportId": obj.ReportId,
                    "CategoryId": obj.CategoryId,
                    "ListingName": obj.Name,
                    "DataColumns": columns if columns else []
                }
                listing.append(obj_dict)

            print(f"Successfully fetched {len(listing)} fields_data")
            return listing

        except Exception as e:
            print(f"Error fetching fields: {e}")
            return []
        
    def get_gold5_listing(self) -> List[Dict[str, Any]]:
        """Get all fields from the gold5listing table

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            # Use direct query since QueryHelper might not be available
            listing_data = self.db.execute_query(QueryHelper.GetListingFromGold5Listing)

            # Convert tuples to dictionaries for better handling
            listing = []
            for obj in listing_data:
                # Column names: OwnerId, RoleId, Name
                columns = [item.strip() for item in obj.DisplayFields.split(",")]
                obj_dict = {
                    "ListingTypeId": obj.ListingTypeID,
                    "RelatedToTypeId": obj.RelatedToTypeID,
                    "DataColumns": columns
                }
                listing.append(obj_dict)

            print(f"Successfully fetched {len(listing)} fields_data")
            return listing

        except Exception as e:
            print(f"Error fetching fields: {e}")
            return []
        

        

    def get_object_relation_listing(self) -> List[Dict[str, Any]]:
        """Get all fields from the objectrelationship table

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            # Use direct query since QueryHelper might not be available
            listing_data = self.db.execute_query(QueryHelper.GetListingFromObjectRelationship)

            # Convert tuples to dictionaries for better handling
            #listingtype,RelatedKeyID, RelationShipID, RelationShipName
            listing = []
            for obj in listing_data:
                # Column names: OwnerId, RoleId, Name
                
                object_name = self.get_object_enum_by_object_id(obj.keyid)
                obj_dict = {
                    "ObjectId": obj.keyid,
                    "ObjectName": object_name,
                    "listingtype": obj.listingtype,
                    "RelatedKeyID": obj.RelatedKeyID,
                    "RelationShipID": obj.RelationShipID,
                    "RelationShipName": obj.RelationShipName,
                    
                    "ModifiedListingName": f"{object_name} {obj.RelationShipName}"
                }
                listing.append(obj_dict)

            print(f"Successfully fetched {len(listing)} fields_data")
            return listing

        except Exception as e:
            print(f"Error fetching fields: {e}")
            return []