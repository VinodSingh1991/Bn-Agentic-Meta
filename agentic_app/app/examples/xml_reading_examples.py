"""
XML Reading Examples - Different approaches for various use cases
"""

# Method 1: Using xml.etree.ElementTree (Most Common)
def read_xml_with_elementtree():
    """Basic XML reading with ElementTree"""
    import xml.etree.ElementTree as ET
    
    # Sample XML content
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <employees>
        <employee id="1">
            <name>John Doe</name>
            <position>Developer</position>
            <salary currency="USD">75000</salary>
        </employee>
        <employee id="2">
            <name>Jane Smith</name>
            <position>Manager</position>
            <salary currency="USD">85000</salary>
        </employee>
    </employees>"""
    
    print("Method 1: ElementTree")
    print("-" * 30)
    
    try:
        # Parse XML string
        root = ET.fromstring(xml_content)
        print(f"Root element: {root.tag}")
        
        # Iterate through employees
        for employee in root.findall('employee'):
            emp_id = employee.get('id')
            name = employee.find('name').text
            position = employee.find('position').text
            salary = employee.find('salary').text
            currency = employee.find('salary').get('currency')
            
            print(f"Employee {emp_id}: {name}, {position}, {salary} {currency}")
    
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")


# Method 2: Using xml.dom.minidom (DOM approach)
def read_xml_with_minidom():
    """Reading XML with minidom (DOM approach)"""
    import xml.dom.minidom as minidom
    
    xml_content = """<?xml version="1.0"?>
    <catalog>
        <book id="bk101">
            <title>XML Developer's Guide</title>
            <author>Gambardella, Matthew</author>
            <price>44.95</price>
        </book>
        <book id="bk102">
            <title>Midnight Rain</title>
            <author>Ralls, Kim</author>
            <price>5.95</price>
        </book>
    </catalog>"""
    
    print("\nMethod 2: MiniDOM")
    print("-" * 30)
    
    try:
        # Parse XML string
        dom = minidom.parseString(xml_content)
        
        # Get book elements
        books = dom.getElementsByTagName('book')
        
        for book in books:
            book_id = book.getAttribute('id')
            title = book.getElementsByTagName('title')[0].firstChild.nodeValue
            author = book.getElementsByTagName('author')[0].firstChild.nodeValue
            price = book.getElementsByTagName('price')[0].firstChild.nodeValue
            
            print(f"Book {book_id}: {title} by {author} - ${price}")
    
    except Exception as e:
        print(f"Error: {e}")


# Method 3: Using BeautifulSoup (Third-party library)
def read_xml_with_beautifulsoup():
    """Reading XML with BeautifulSoup (requires installation)"""
    print("\nMethod 3: BeautifulSoup")
    print("-" * 30)
    
    try:
        from bs4 import BeautifulSoup
        
        xml_content = """<?xml version="1.0"?>
        <products>
            <product category="electronics">
                <name>Laptop</name>
                <price>999.99</price>
                <stock>25</stock>
            </product>
            <product category="books">
                <name>Python Guide</name>
                <price>29.99</price>
                <stock>100</stock>
            </product>
        </products>"""
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(xml_content, 'xml')
        
        # Find all products
        products = soup.find_all('product')
        
        for product in products:
            category = product.get('category')
            name = product.name.text
            price = product.price.text
            stock = product.stock.text
            
            print(f"Product: {name} ({category}) - ${price}, Stock: {stock}")
    
    except ImportError:
        print("BeautifulSoup not installed. Install with: pip install beautifulsoup4 lxml")
    except Exception as e:
        print(f"Error: {e}")


# Method 4: Reading from file
def read_xml_from_file():
    """Example of reading XML from file"""
    import xml.etree.ElementTree as ET
    import tempfile
    import os
    
    print("\nMethod 4: Reading from File")
    print("-" * 30)
    
    # Create a temporary XML file
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <database>
            <host>localhost</host>
            <port>5432</port>
            <name>myapp</name>
        </database>
        <logging>
            <level>INFO</level>
            <file>app.log</file>
        </logging>
    </configuration>"""
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_file = f.name
        
        # Read XML file
        tree = ET.parse(temp_file)
        root = tree.getroot()
        
        print(f"Configuration loaded from: {temp_file}")
        
        # Parse database config
        db_config = root.find('database')
        if db_config is not None:
            host = db_config.find('host').text
            port = db_config.find('port').text
            name = db_config.find('name').text
            print(f"Database: {host}:{port}/{name}")
        
        # Parse logging config
        log_config = root.find('logging')
        if log_config is not None:
            level = log_config.find('level').text
            file = log_config.find('file').text
            print(f"Logging: {level} -> {file}")
        
        # Clean up
        os.unlink(temp_file)
    
    except Exception as e:
        print(f"Error: {e}")


# Method 5: Advanced XML parsing with namespaces
def read_xml_with_namespaces():
    """Reading XML with namespaces"""
    import xml.etree.ElementTree as ET
    
    xml_content = """<?xml version="1.0"?>
    <root xmlns:app="http://myapp.com/schema" xmlns:cfg="http://config.com/schema">
        <app:application>
            <app:name>MyApp</app:name>
            <app:version>1.0</app:version>
        </app:application>
        <cfg:config>
            <cfg:debug>true</cfg:debug>
            <cfg:timeout>30</cfg:timeout>
        </cfg:config>
    </root>"""
    
    print("\nMethod 5: XML with Namespaces")
    print("-" * 30)
    
    try:
        root = ET.fromstring(xml_content)
        
        # Define namespaces
        namespaces = {
            'app': 'http://myapp.com/schema',
            'cfg': 'http://config.com/schema'
        }
        
        # Find elements with namespaces
        app_info = root.find('app:application', namespaces)
        if app_info is not None:
            name = app_info.find('app:name', namespaces).text
            version = app_info.find('app:version', namespaces).text
            print(f"Application: {name} v{version}")
        
        config_info = root.find('cfg:config', namespaces)
        if config_info is not None:
            debug = config_info.find('cfg:debug', namespaces).text
            timeout = config_info.find('cfg:timeout', namespaces).text
            print(f"Config: Debug={debug}, Timeout={timeout}s")
    
    except Exception as e:
        print(f"Error: {e}")


# Method 6: Converting XML to JSON
def xml_to_json_conversion():
    """Convert XML to JSON format"""
    import xml.etree.ElementTree as ET
    import json
    
    xml_content = """<?xml version="1.0"?>
    <menu>
        <item id="1" type="burger">
            <name>Big Mac</name>
            <price>5.99</price>
            <calories>550</calories>
        </item>
        <item id="2" type="drink">
            <name>Coke</name>
            <price>1.99</price>
            <calories>140</calories>
        </item>
    </menu>"""
    
    print("\nMethod 6: XML to JSON Conversion")
    print("-" * 30)
    
    def xml_to_dict(element):
        """Convert XML element to dictionary"""
        result = {}
        
        # Add attributes
        if element.attrib:
            result.update(element.attrib)
        
        # Add text content
        if element.text and element.text.strip():
            if len(element) == 0:
                return element.text.strip()
            else:
                result['text'] = element.text.strip()
        
        # Add child elements
        for child in element:
            child_data = xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result
    
    try:
        root = ET.fromstring(xml_content)
        json_data = {root.tag: xml_to_dict(root)}
        
        print("XML converted to JSON:")
        print(json.dumps(json_data, indent=2))
    
    except Exception as e:
        print(f"Error: {e}")


# Main demonstration
def main():
    """Run all XML reading examples"""
    print("XML Reading in Python - Complete Examples")
    print("=" * 50)
    
    read_xml_with_elementtree()
    read_xml_with_minidom()
    read_xml_with_beautifulsoup()
    read_xml_from_file()
    read_xml_with_namespaces()
    xml_to_json_conversion()
    
    print("\n" + "=" * 50)
    print("All examples completed!")


if __name__ == "__main__":
    main()