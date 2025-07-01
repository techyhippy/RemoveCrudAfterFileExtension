# Remove Crud After File Extension

This is a NZBGet post-processing script that removes extra characters after file extensions for supported media files.

## Supported File Types

- Video files: `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`
- Subtitle files: `.srt`, `.sub`, `.ass`, `.ssa`, `.vtt`
- Image files: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`

## Installation

1. Download the extension from GitHub:
   ```bash
   wget https://github.com/techyhippy/RemoveCrudAfterFileExtension/archive/refs/heads/main.zip
   ```

2. Extract the downloaded zip file:
   ```bash
   unzip main.zip
   ```

3. Copy the extension to your NZBGet scripts directory:
   ```bash
   cp -r RemoveCrudAfterFileExtension-main/* /config/scripts/RemoveCrudAfterFileExtension/
   ```

4. Make the script executable:
   ```bash
   chmod +x /config/scripts/RemoveCrudAfterFileExtension/remove_crud.py
   ```

## Usage

The script will automatically run as a NZBGet post-processing script. It will process files in the download directory after they are completed.

## NZBGet Configuration

1. Copy the extension files to `/config/scripts/RemoveCrudAfterFileExtension/`
2. Make sure the script is executable:
   ```bash
   chmod +x /config/scripts/RemoveCrudAfterFileExtension/remove_crud.py
   ```
3. Restart NZBGet:
   ```bash
   docker restart nzbget
   ```
4. The extension should automatically appear in the Extensions section of the web interface

## Exit Codes

- `90`: Success (NZBGet standard)
- `91`: Error (NZBGet standard)
- `93`: Directory not found

## Example

Before:
```
filename.mp4_extra.dfdf.dfg. sdssds
```

After:
```
filename.mp4
```

## Logging

The script logs all operations to the NZBGet log file. You can view the logs in NZBGet's web interface or through the command line.
