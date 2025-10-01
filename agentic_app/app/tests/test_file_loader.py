"""
Test script to verify FileLoader path resolution
"""
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.files_handler.file_loader import FileLoader

def test_file_loader():
    """Test the FileLoader path resolution"""
    
    print("Testing FileLoader path resolution...")
    
    # Test with default path (automatic resolution)
    loader = FileLoader()
    
    print(f"Resolved folder path: {loader.get_folder_path()}")
    print(f"Folder exists: {loader.validate_folder_path()}")
    
    # Test loading files
    if loader.validate_folder_path():
        try:
            data = loader.get_file_data()
            print(f"Successfully loaded {len(data)} JSON files:")
            for filename in data.keys():
                print(f"  - {filename}")
        except Exception as e:
            print(f"Error loading files: {e}")
    else:
        print("Folder path is not valid - creating directory...")
        try:
            os.makedirs(loader.folder_path, exist_ok=True)
            print(f"Created directory: {loader.folder_path}")
        except Exception as e:
            print(f"Failed to create directory: {e}")

if __name__ == "__main__":
    test_file_loader()