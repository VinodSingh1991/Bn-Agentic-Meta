from repositories.get_listing_repository import ListingRepository
from files_handler.file_loader import FileLoader
from typing import List, Any

class ListingService:
    def __init__(self):
        self.repository = ListingRepository()
        self.loader = FileLoader()

    def get_listing_base(self) -> List[Any]:
        try:
            result = self.repository.get_rpt_listing()
            # Save the result to JSON file using the correct method name
            self.loader.save_files_at_orignal("listing_rpt.json", result)
            return result
        except Exception as e:
            print(f"Error in ListingService.get_listing: {e}")
            return []
        
        
    def get_rpt_listing(self) -> List[Any]:

        result = self.get_listing_base()

        return result
    
    def get_gold5_listing_base(self) -> List[Any]:
        try:
            result = self.repository.get_gold5_listing()
            # Save the result to JSON file using the correct method name
            self.loader.save_files_at_orignal("listing_gold5.json", result)
            return result
        except Exception as e:
            print(f"Error in ListingService.get_gold5_listing: {e}")
            return []
        
        
    def get_gold5_listing(self) -> List[Any]:
        result = self.get_gold5_listing_base()
        return result
    
    def get_field_by_fieldName_with_object_name(self, fieldList, object_name) -> List[Any]:
        fields = []
        try:
            all_fields = self.loader.loadJsonFile("fields.json")
            for field in fieldList:
                field_info = next((f for f in all_fields if f.get("FieldName") == field and f.get("ObjectName") == object_name), None)
                if field_info:
                    extended_field_info = {}
                    extended_field_info["roleid"] = 1
                    extended_field_info["object_name"] = object_name
                    extended_field_info["field_id"] = field_info.get("FieldId", "")
                    extended_field_info["name"] = field_info.get("Label", "")
                    extended_field_info["FieldName"] = field_info.get("FieldName", "")
                    extended_field_info["field_type"] = field_info.get("FieldType", "Text")
                    fields.append(extended_field_info)
            return fields
        except Exception as e:
            print(f"Error in ListingService.get_field_by_fieldName_with_object_name: {e}")
            return fields
            
    def map_object_and_gold5_listing(self) -> List[Any]:
        try:
            newListing = []
            
            object_relation = self.loader.loadJsonFile("listing_object_relationship.json")
            gold5_listing = self.loader.loadJsonFile("listing_gold5.json")
            
            if gold5_listing:
                for listing in gold5_listing:
                    list_id = listing.get("ListingTypeId")
                    object_id = listing.get("RelatedToTypeId")
                    
                    if object_id and object_relation:
                        related_object = next((obj for obj in object_relation if obj.get("ObjectId") == object_id and obj.get("listingtype") == list_id), None)
                        if related_object:
                            listing_modified = {}
                            listing_modified["ListingName"] = related_object.get("RelationShipName", "")
                            listing_modified["RelatedName"] = related_object.get("ModifiedListingName", "")
                            listing_modified["ObjectId"] = related_object.get("ObjectId", "")
                            listing_modified["ObjectName"] = related_object.get("ObjectName", "")
                            cols = listing.get("DataColumns", [])
                            object_name = related_object.get("ObjectName", "")
                            fields = self.get_field_by_fieldName_with_object_name(cols, object_name)
                            newListing.append({
                                "query_label": related_object.get("ModifiedListingName", ""),
                                "query_field": fields
                            })


            self.loader.save_files_at_output("listing_gold5.json", newListing)
            return newListing

        except Exception as e:
            print(f"Error in ListingService.get_object_relation_listing: {e}")
            return []
        
    def map_object_and_rpt_listing(self) -> List[Any]:
        try:
            newListing = []
            
            rpt_listing = self.loader.loadJsonFile("listing_rpt.json")

            if rpt_listing:
                for listing in rpt_listing:
                    object_name = listing.get("ObjectName", "")
                    cols = listing.get("DataColumns", [])
                    listing_name = listing.get("ListingName", "")
                    fields = self.get_field_by_fieldName_with_object_name(cols, object_name)
                    newListing.append({
                        "query_label": listing_name,
                        "query_field": fields
                    })

            self.loader.save_files_at_output("listing_rpt.json", newListing)
            return newListing

        except Exception as e:
            print(f"Error in ListingService.get_object_relation_listing: {e}")
            return []
    
    def get_object_relation_listing(self) -> List[Any]:
        try:
            result = self.repository.get_object_relation_listing()
            # Save the result to JSON file using the correct method name
            self.loader.save_files_at_orignal("listing_object_relationship.json", result)
            return result
        except Exception as e:
            print(f"Error in ListingService.get_object_relation_listing: {e}")
            return []
        
        
        