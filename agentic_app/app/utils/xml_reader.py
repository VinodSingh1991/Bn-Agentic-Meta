"""
XML Reader Implementation for Python
Provides multiple ways to read and parse XML files
"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional

class XMLReader:
    """
    A comprehensive XML reader class with multiple parsing methods
    """
    
    def __init__(self):
        self.parsed_data = {}
  
    def read_xml_string(self, xml_string: str) -> Optional[ET.Element]:
        """
        Read XML from string
        
        Args:
            xml_string (str): XML content as string
            
        Returns:
            Optional[ET.Element]: Root element or None if error
        """
        try:
            root = ET.fromstring(xml_string)
            return root
            
        except ET.ParseError as e:
            print(f"XML Parse Error: {e}")
            return None
        except Exception as e:
            print(f"Error parsing XML string: {e}")
            return None
    
    def xml_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """
        Convert XML element to dictionary recursively
        
        Args:
            element (ET.Element): XML element to convert
            
        Returns:
            Dict[str, Any]: Dictionary representation of XML
        """
        result = {}
        
        # Add attributes
        if element.attrib:
            result['@attributes'] = element.attrib
        
        # Add text content
        if element.text and element.text.strip():
            if len(element) == 0:  # No child elements
                return element.text.strip()
            else:
                result['#text'] = element.text.strip()
        
        # Add child elements
        children = {}
        for child in element:
            child_data = self.xml_to_dict(child)
            
            if child.tag in children:
                # Multiple elements with same tag - convert to list
                if not isinstance(children[child.tag], list):
                    children[child.tag] = [children[child.tag]]
                children[child.tag].append(child_data)
            else:
                children[child.tag] = child_data
        
        result.update(children)
        return result

    def find_elements(self, root: ET.Element, tag_name: str, direct_child_only: bool = False) -> List[ET.Element]:
        """
        Find all elements with specific tag name
        
        Args:
            root (ET.Element): Root element to search in
            tag_name (str): Tag name to search for
            
        Returns:
            List[ET.Element]: List of matching elements
        """
        try:
            if direct_child_only:
                elements = root.findall(f"./{tag_name}")
            else:
                elements = root.findall(f".//{tag_name}")
            return elements
        except Exception as e:
            print(f"Error finding elements: {e}")
            return []
    
    def find_element_by_attribute(self, root: ET.Element, tag_name: str, 
                                attr_name: str, attr_value: str) -> Optional[ET.Element]:
        """
        Find element by tag name and attribute value
        
        Args:
            root (ET.Element): Root element to search in
            tag_name (str): Tag name to search for
            attr_name (str): Attribute name
            attr_value (str): Attribute value
            
        Returns:
            Optional[ET.Element]: Matching element or None
        """
        try:
            xpath = f".//{tag_name}[@{attr_name}='{attr_value}']"
            element = root.find(xpath)
            if element is not None:
                print(f"Found element {tag_name} with {attr_name}='{attr_value}'")
            return element
        except Exception as e:
            print(f"Error finding element by attribute: {e}")
            return None

    def get_element_attribute(self, element: ET.Element, attr_name: str, 
                            default: str = "") -> str:
        """
        Get attribute value safely
        
        Args:
            element (ET.Element): Element to get attribute from
            attr_name (str): Attribute name
            default (str): Default value if attribute not found
            
        Returns:
            str: Attribute value or default
        """
        if element is not None:
            return element.get(attr_name, default)
        return default
    
