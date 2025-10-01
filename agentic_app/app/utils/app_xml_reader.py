"""
Application-specific XML Reader
Integrates with the existing file_loader structure
"""

from .xml_reader import XMLReader
from files_handler.file_loader import FileLoader
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional
import os
import json


class AppXMLReader(XMLReader):
    """
    Application-specific XML reader that integrates with FileLoader
    """
    
    def __init__(self):
        super().__init__()
        self.file_loader = FileLoader()
    
    def read_xml_files_from_directory(self, directory_path: str = None) -> Dict[str, Any]:
        """
        Read all XML files from a directory (similar to load_json_files)
        
        Args:
            directory_path (str): Directory path, uses FileLoader default if None
            
        Returns:
            Dict[str, Any]: Dictionary with filename as key and XML content as value
        """
        if directory_path is None:
            directory_path = self.file_loader.folder_path
        
        xml_data = {}
        
        try:
            if not os.path.exists(directory_path):
                print(f"Directory does not exist: {directory_path}")
                return xml_data
            
            for filename in os.listdir(directory_path):
                if filename.lower().endswith('.xml'):
                    file_path = os.path.join(directory_path, filename)
                    
                    try:
                        # Read XML and convert to dictionary
                        xml_dict = self.read_xml_to_dict(file_path)
                        if xml_dict:
                            xml_data[filename] = xml_dict
                            print(f"Loaded XML file: {filename}")
                        
                    except Exception as e:
                        print(f"Error loading XML file {filename}: {e}")
            
            print(f"Successfully loaded {len(xml_data)} XML files")
            return xml_data
            
        except Exception as e:
            print(f"Error reading XML files from directory: {e}")
            return xml_data
    
    def save_xml_as_json(self, xml_filename: str, json_filename: str = None) -> bool:
        """
        Convert XML file to JSON and save using FileLoader
        
        Args:
            xml_filename (str): Name of XML file to convert
            json_filename (str): Output JSON filename, auto-generated if None
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if json_filename is None:
                json_filename = xml_filename.replace('.xml', '.json')
            
            xml_path = os.path.join(self.file_loader.folder_path, xml_filename)
            
            if not os.path.exists(xml_path):
                print(f"XML file not found: {xml_path}")
                return False
            
            # Convert XML to dictionary
            xml_dict = self.read_xml_to_dict(xml_path)
            
            if xml_dict:
                # Save using FileLoader
                self.file_loader.save_files(json_filename, xml_dict)
                print(f"Successfully converted {xml_filename} to {json_filename}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error saving XML as JSON: {e}")
            return False
    
    def parse_layout_xml(self, xml_content: str) -> Dict[str, Any]:
        """
        Parse layout-specific XML content
        Customize this based on your XML structure
        
        Args:
            xml_content (str): XML content string
            
        Returns:
            Dict[str, Any]: Parsed layout data
        """
        try:
            root = self.read_xml_string(xml_content)
            if not root:
                return {}
            
            layout_data = {
                'layout_id': self.get_element_attribute(root, 'id'),
                'layout_name': self.get_element_attribute(root, 'name'),
                'components': [],
                'properties': {}
            }
            
            # Parse components
            components = self.find_elements(root, 'component')
            for component in components:
                comp_data = {
                    'id': self.get_element_attribute(component, 'id'),
                    'type': self.get_element_attribute(component, 'type'),
                    'properties': {}
                }
                
                # Parse component properties
                for prop in component:
                    comp_data['properties'][prop.tag] = prop.text
                
                layout_data['components'].append(comp_data)
            
            # Parse layout properties
            properties = root.find('properties')
            if properties is not None:
                for prop in properties:
                    layout_data['properties'][prop.tag] = prop.text
            
            return layout_data
            
        except Exception as e:
            print(f"Error parsing layout XML: {e}")
            return {}
    
    def parse_config_xml(self, xml_file_path: str) -> Dict[str, Any]:
        """
        Parse configuration XML file
        
        Args:
            xml_file_path (str): Path to XML configuration file
            
        Returns:
            Dict[str, Any]: Configuration data
        """
        try:
            root = self.read_xml_file(xml_file_path)
            if not root:
                return {}
            
            config = {}
            
            # Parse database configuration
            db_config = root.find('database')
            if db_config is not None:
                config['database'] = {
                    'server': self.get_element_text(db_config.find('server')),
                    'database': self.get_element_text(db_config.find('database')),
                    'username': self.get_element_text(db_config.find('username')),
                    'password': self.get_element_text(db_config.find('password'))
                }
            
            # Parse application settings
            app_settings = root.find('application')
            if app_settings is not None:
                config['application'] = {}
                for setting in app_settings:
                    config['application'][setting.tag] = setting.text
            
            return config
            
        except Exception as e:
            print(f"Error parsing config XML: {e}")
            return {}
    
    def export_data_to_xml(self, data: Dict[str, Any], filename: str, 
                          root_element: str = 'data') -> bool:
        """
        Export dictionary data to XML file
        
        Args:
            data (Dict[str, Any]): Data to export
            filename (str): Output XML filename
            root_element (str): Root element name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            def dict_to_xml_element(parent, key, value):
                """Recursively convert dictionary to XML elements"""
                if isinstance(value, dict):
                    element = ET.SubElement(parent, key)
                    for k, v in value.items():
                        dict_to_xml_element(element, k, v)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            element = ET.SubElement(parent, key)
                            for k, v in item.items():
                                dict_to_xml_element(element, k, v)
                        else:
                            element = ET.SubElement(parent, key)
                            element.text = str(item)
                else:
                    element = ET.SubElement(parent, key)
                    element.text = str(value) if value is not None else ''
            
            # Create root element
            root = ET.Element(root_element)
            
            # Convert data to XML elements
            for key, value in data.items():
                dict_to_xml_element(root, key, value)
            
            # Create tree and save
            tree = ET.ElementTree(root)
            output_path = os.path.join(self.file_loader.output_path, filename)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write XML file with proper formatting
            ET.indent(tree, space="  ", level=0)  # Python 3.9+
            tree.write(output_path, encoding='utf-8', xml_declaration=True)
            
            print(f"Successfully exported data to XML: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting data to XML: {e}")
            return False


# Example usage function
def example_xml_usage():
    """Example of how to use the XML reader in your application"""
    
    print("Application XML Reader Example")
    print("=" * 40)
    
    # Initialize XML reader
    xml_reader = AppXMLReader()
    
    # Example 1: Read all XML files from directory
    print("\n1. Reading XML files from directory:")
    xml_files = xml_reader.read_xml_files_from_directory()
    print(f"Found {len(xml_files)} XML files")
    
    # Example 2: Convert XML to JSON
    print("\n2. Converting XML to JSON:")
    # xml_reader.save_xml_as_json('config.xml', 'config.json')
    
    # Example 3: Parse sample layout XML
    sample_layout_xml = """<?xml version="1.0"?>
    <layout id="dashboard" name="Main Dashboard">
        <properties>
            <width>1200</width>
            <height>800</height>
            <theme>dark</theme>
        </properties>
        <component id="header" type="navbar">
            <title>Dashboard</title>
            <position>top</position>
        </component>
        <component id="sidebar" type="menu">
            <width>250</width>
            <position>left</position>
        </component>
    </layout>"""
    
    print("\n3. Parsing layout XML:")
    layout_data = xml_reader.parse_layout_xml(sample_layout_xml)
    print(json.dumps(layout_data, indent=2))
    
    # Example 4: Export data to XML
    print("\n4. Exporting data to XML:")
    sample_data = {
        'roles': [
            {'id': 1, 'name': 'Admin', 'permissions': ['read', 'write', 'delete']},
            {'id': 2, 'name': 'User', 'permissions': ['read']}
        ],
        'settings': {
            'theme': 'dark',
            'language': 'en',
            'timezone': 'UTC'
        }
    }
    
    xml_reader.export_data_to_xml(sample_data, 'exported_data.xml', 'application_data')


if __name__ == "__main__":
    example_xml_usage()