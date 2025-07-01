#!/lsiopy/bin/python3

###########################################
### NZBGET POST-PROCESSING SCRIPT       ###
# This is a NZBGet post-processing script 
# that removes extra characters after file 
# extensions for supported media files.
#

### NZBGET POST-PROCESSING SCRIPT       ###
###########################################

import os
import sys
import logging
from typing import List, Set

# NZBGet environment variables
NZBPP_DIRECTORY = os.environ.get('NZBPP_DIRECTORY', '')
NZBPP_NZBNAME = os.environ.get('NZBPP_NZBNAME', '')
NZBPP_PARTSIZE = os.environ.get('NZBPP_PARTSIZE', '0')
NZBPP_STATUS = os.environ.get('NZBPP_STATUS', '')
NZBPP_CATEGORY = os.environ.get('NZBPP_CATEGORY', '')
NZBPP_PARSTATUS = os.environ.get('NZBPP_PARSTATUS', '')
NZBPP_UNPACKSTATUS = os.environ.get('NZBPP_UNPACKSTATUS', '')
NZBPP_URL = os.environ.get('NZBPP_URL', '')
NZBPP_SCRIPTDIR = os.environ.get('NZBPP_SCRIPTDIR', '')
NZBPP_VERSION = os.environ.get('NZBPP_VERSION', '')
NZBPP_BRANCH = os.environ.get('NZBPP_BRANCH', '')
NZBPP_BUILD = os.environ.get('NZBPP_BUILD', '')
NZBPP_URLS = os.environ.get('NZBPP_URLS', '')

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
            logging.info(f"Cleaned filename: {filename} -> {clean_name}")
            return clean_name
        logging.info(f"Unsupported extension: {ext}")
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
                # Get filename and clean it
                filename = os.path.basename(file_path)
                logging.info(f"Processing file: {filename}")
                
                # Check if file exists
                if not os.path.exists(file_path):
                    logging.error(f"File does not exist: {file_path}")
                    continue

                clean_name = clean_filename(filename)
                
                if clean_name != filename:
                    new_path = os.path.join(directory, clean_name)
                    
                    # Check if target file already exists
                    if os.path.exists(new_path):
                        logging.warning(f"Target file already exists: {new_path}")
                        continue
                    
                    # Rename the file
                    try:
                        os.rename(file_path, new_path)
                        logging.info(f"Renamed: {filename} -> {clean_name}")
                    except Exception as e:
                        logging.error(f"Error renaming file {file_path} to {new_path}: {e}")
                else:
                    logging.info(f"No changes needed for: {filename}")
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
                logging.error(f"Full traceback: {traceback.format_exc()}")
        
        return NZBGET_OK
    except Exception as e:
        logging.error(f"Error processing directory {directory}: {e}")
        logging.error(f"Full traceback: {traceback.format_exc()}")
        return NZBGET_ERROR

def main():
    """Main entry point for NZBGet post-processing script."""
    try:
        # Log script start with environment variables
        logging.info("RemoveCrud extension started")
        logging.info(f"Environment variables: NZBPO_ENABLED={os.getenv('NZBPO_ENABLED')}, NZBPP_DIRECTORY={os.getenv('NZBPP_DIRECTORY')}")
        logging.info(f"Script path: {os.path.abspath(__file__)}")
        logging.info(f"Python version: {sys.version}")
        
        # Get directory from NZBGet environment variable
        directory = os.getenv('NZBPP_DIRECTORY', '')
        if not directory:
            logging.error("Directory not provided")
            return NZBGET_ERROR

        # Log directory being processed
        logging.info(f"Processing directory: {directory}")

        # Check if enabled
        enabled = os.getenv('NZBPO_ENABLED', 'Yes').upper()
        if enabled != 'YES':
            logging.info("RemoveCrud Extension is disabled")
            return NZBGET_DISABLED

        # Process the directory
        exit_code = process_directory(directory)
        
        # Log script completion
        logging.info("RemoveCrud extension completed")
        return exit_code

    except Exception as e:
        logging.error(f"Error processing directory: {e}")
        logging.error(f"Full traceback: {traceback.format_exc()}")
        return NZBGET_ERROR

if __name__ == "__main__":
    sys.exit(main())
