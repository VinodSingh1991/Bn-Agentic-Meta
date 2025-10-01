from csv import reader
from utils.layout_helper import LayoutHelper
from repositories.get_layouts_repository import LayoutRepository
from files_handler.file_loader import FileLoader
from typing import List, Any, Dict


class LayoutService:
    def __init__(self):
        self.repository = LayoutRepository()
        self.loader = FileLoader()
        self.layout_helper = LayoutHelper()


    def get_layouts_base(self) -> List[Dict[str, Any]]:
        """
        Get all layouts with role mapping and UI master information
        
        Returns:
            List[Dict[str, Any]]: List of layout dictionaries with combined information
        """
        try:
            
            local_data = self.loader.loadJsonFile("layouts.json")
            if local_data:
                return local_data
        
            # Fetch all required data
            layout_group = self.repository.get_layout_group()
            layout_ui_master = self.repository.get_layout_ui_master()
            layout_role_mapping = self.repository.get_layout_role_mapping()

            layouts = []
            
            if layout_group:
                for layout in layout_group:
                    # Create a copy of the layout to avoid modifying the original
                    enriched_layout = dict(layout) if isinstance(layout, dict) else layout

                    # Find matching UI master information
                    ui_master = next(
                        (ui for ui in layout_ui_master if ui.get("LayoutID") == layout.get("LayoutID")),
                        None
                    )
                    
                    if ui_master and isinstance(ui_master, dict):
                        # Add UI master information to the layout
                        enriched_layout["LayoutName"] = ui_master.get("UIName", "Unknown")
                    else:
                        enriched_layout["LayoutName"] = "Unknown"
                        
                    # Find matching role mapping
                    role_mapping = next(
                        (r for r in layout_role_mapping if r.get("LayoutId") == layout.get("LayoutID")),
                        None
                    )

                    if role_mapping and isinstance(role_mapping, dict):
                        roleid = role_mapping.get("RoleId", 1)
                        enriched_layout["RoleId"] = roleid
                    else:
                        enriched_layout["RoleId"] = 1

                    xml_json = self.layout_helper.get_field_from_xml(layout.get("LayoutXML", ""), enriched_layout.get("RoleId"))
                    enriched_layout["LayoutFields"] = xml_json
                    enriched_layout["LayoutXML"] = ""
                    layouts.append(enriched_layout)

            # Save to file using the correct method name
            try:
                self.loader.save_files_at_orignal("layouts.json", layouts)
                print(f"Successfully saved {len(layouts)} layouts to file")
            except Exception as save_error:
                print(f"Warning: Could not save layouts to file: {save_error}")
            
            return layouts
            
        except Exception as e:
            print(f"Error in LayoutService.get_layouts: {e}")
            return []
        
    def get_layouts(self) -> Dict[str, Any]:
        """
        Process layouts and create consolidated field information
        
        Returns:
            Dict[str, Any]: Dictionary of consolidated layout fields
        """

        layouts = self.get_layouts_base()
            
        return layouts

    def create_layouts(self) -> Dict[str, Any]:
        result = self.repository.get_layouts_file()
        extracted_field = self.layout_helper.build_layout_fields(result)
        self.loader.save_files_at_output("layouts_fields.json", extracted_field)
        return extracted_field