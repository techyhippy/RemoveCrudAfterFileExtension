# Remove Crud After File Extension

This NZBGet post-processing script removes extra characters after file extensions for supported media files.

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
   cp -r RemoveCrudAfterFileExtension-main/* /usr/local/share/nzbget/scripts/RemoveCrudAfterFileExtension/
   ```

4. Make the script executable:
   ```bash
   chmod +x /usr/local/share/nzbget/scripts/RemoveCrudAfterFileExtension/remove_crud.py
   ```

## Usage

The script will automatically run as a NZBGet post-processing script. It will process files in the download directory after they are completed.

## NZBGet Configuration

Add the following to your NZBGet configuration:

```ini
[Script]
ScriptEnable=postdownload
ScriptPostDownload=/usr/local/share/nzbget/scripts/remove_crud.py
```

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
