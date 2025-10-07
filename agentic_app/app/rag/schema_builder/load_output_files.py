from files_handler.rag_file_loader import RagFileLoader
from typing import Dict, Any, List

class LoadOutputFiles:
    def __init__(self):
        self.rag_file_loader = RagFileLoader()
        
    def load_layout_files(self):
        try:
            new_layouts = []
            layouts = self.rag_file_loader.load_all_layout_files_at_output()
            if layouts:
                for layout in layouts.values():
                    if isinstance(layout, list):
                        new_layouts.extend(layout)
                    else:
                        new_layouts.append(layout)
            return new_layouts
        except Exception as e:
            print(f"Error loading layout files: {e}")
            return []
        
    def load_fields_file(self):
        try:
            fields = self.rag_file_loader.load_file_at_output("fields.json")
            return fields
        except Exception as e:
            print(f"Error loading fields file: {e}")
            return None
        
    def load_layout_fields_file(self):
        try:
            layout_fields = self.rag_file_loader.load_file_at_output("layout_fields.json")
            return layout_fields
        except Exception as e:
            print(f"Error loading layout fields file: {e}")
            return None
        
    def load_gold5_listings_file(self):
        try:
            gold5_listings = self.rag_file_loader.load_file_at_output("listing_gold5.json")
            return gold5_listings
        except Exception as e:
            print(f"Error loading gold5 listings file: {e}")
            return []
        
    def load_rpt_listings_file(self):
        try:
            rpt_listings = self.rag_file_loader.load_file_at_output("listing_rpt.json")
            return rpt_listings
        except Exception as e:
            print(f"Error loading rpt listings file: {e}")
            return []

    def save_files_for_layouts(self, filename: str, data: Any):
        try:
            self.rag_file_loader.save_files_at_rag_output(filename, data)
        except Exception as e:
            print(f"Error saving file {filename}: {e}")
            
    def save_file_at_rag_output(self, filename: str, data: Any):
        try:
            self.rag_file_loader.save_files_at_rag_output(filename, data)
        except Exception as e:
            print(f"Error saving file {filename}: {e}")
            
    def get_all_layouts_and_listings(self) -> List[Any]:
        try:
            layouts = self.load_layout_files() or []
            gold5_listings = self.load_gold5_listings_file() or []
            rpt_listings = self.load_rpt_listings_file() or []
            all_items = layouts + gold5_listings + rpt_listings
            return all_items
        except Exception as e:
            print(f"Error getting all layouts and listings: {e}")
            return []
        
    def get_all_fields(self) -> List[Any]:
        try:
            field = self.load_fields_file() or []
            layout_fields = self.load_layout_fields_file() or []

            all_items = field + layout_fields
            return all_items
        except Exception as e:
            print(f"Error getting all layouts and listings: {e}")
            return []
        
    def get_all_data(self) -> List[Any]:
        try:
            layouts = self.get_all_layouts_and_listings() or []
            fields = self.get_all_fields() or []

            all_items = layouts + fields
            return all_items
        except Exception as e:
            print(f"Error getting all layouts and listings: {e}")
            return []
