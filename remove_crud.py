import os
import sys
import logging
from typing import List, Set

# NZBGet error codes
NZBGET_OK = 90
NZBGET_ERROR = 91
NZBGET_DIR_NOT_FOUND = 93
NZBGET_DISABLED = 94

# Configure logging
log_level = os.getenv('NZBPO_LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Supported file extensions (case-insensitive)
SUPPORTED_EXTENSIONS: Set[str] = {
    # Video files
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv',
    # Subtitle files
    '.srt', '.sub', '.ass', '.ssa', '.vtt',
    # Image files
    '.jpg', '.jpeg', '.png', '.gif', '.webp'
}

def get_supported_files(directory: str) -> List[str]:
    """Get all supported files in the directory."""
    supported_files = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                # Get file extension (case-insensitive)
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTENSIONS:
                    supported_files.append(os.path.join(root, file))
        return supported_files
    except Exception as e:
        logging.error(f"Error getting supported files: {e}")
        return []

def clean_filename(filename: str) -> str:
    """Clean filename by removing extra characters after the extension."""
    try:
        # Get base name and extension
        base, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # If it's a supported extension, clean it
        if ext in SUPPORTED_EXTENSIONS:
            # Split by extension and take the first part
            clean_name = base.split(ext)[0] + ext
            return clean_name
        return filename
    except Exception as e:
        logging.error(f"Error cleaning filename {filename}: {e}")
        return filename

def process_directory(directory: str) -> int:
    """Process all supported files in the directory."""
    try:
        if not os.path.exists(directory):
            logging.error(f"Directory does not exist: {directory}")
            return NZBGET_DIR_NOT_FOUND

        supported_files = get_supported_files(directory)
        if not supported_files:
            logging.info("No supported files found in directory")
            return NZBGET_OK

        for file_path in supported_files:
            try:
                # Get the parent directory and filename
                parent_dir = os.path.dirname(file_path)
                filename = os.path.basename(file_path)
                
                # Clean the filename
                clean_name = clean_filename(filename)
                
                if clean_name != filename:
                    new_path = os.path.join(parent_dir, clean_name)
                    if os.path.exists(new_path):
                        logging.warning(f"File already exists: {new_path}")
                        continue
                    
                    # Rename the file
                    os.rename(file_path, new_path)
                    logging.info(f"Renamed: {filename} -> {clean_name}")
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")

        return NZBGET_OK
    except Exception as e:
        logging.error(f"Error processing directory {directory}: {e}")
        return NZBGET_ERROR

if __name__ == "__main__":
    # Check if enabled
    enabled = os.getenv('NZBPO_ENABLED', 'Yes').upper()
    if enabled != 'YES':
        logging.info("Extension is disabled")
        sys.exit(NZBGET_DISABLED)

    if len(sys.argv) != 2:
        logging.error("Usage: python remove_crud.py <directory>")
        sys.exit(NZBGET_ERROR)

    directory = sys.argv[1]
    exit_code = process_directory(directory)
    sys.exit(exit_code)
