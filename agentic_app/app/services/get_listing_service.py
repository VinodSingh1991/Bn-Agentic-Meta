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

    def map_object_and_gold5_listing(self) -> List[Any]:
        try:
            newListing = []
            
            object_relation = self.loader.loadJsonFile("listing_object_relationship.json")
            gold5_listing = self.loader.loadJsonFile("listing_gold5.json")
            rpt_listing = self.loader.loadJsonFile("listing_rpt.json")
            
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
                            listing_modified["DataColumns"] = listing.get("DataColumns", [])
                            newListing.append(listing_modified)

            if rpt_listing:
                for rpt_list_item in rpt_listing:
                    if rpt_list_item:
                        listing_modified = {}
                        listing_modified["ListingName"] = rpt_list_item.get("ListingName", "")
                        listing_modified["RelatedName"] = "These are not related listing it is a primary object listing"
                        listing_modified["ObjectId"] = rpt_list_item.get("ObjectId", "")
                        listing_modified["ObjectName"] = rpt_list_item.get("ObjectName", "")
                        listing_modified["DataColumns"] = rpt_list_item.get("DataColumns", [])
                        newListing.append(listing_modified)

            self.loader.save_files_at_output("listing_gold5_enriched.json", newListing)
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
        
        
        