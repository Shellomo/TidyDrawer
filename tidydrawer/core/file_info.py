import os
from datetime import datetime
from hashlib import sha256
from magika import Magika
magika = Magika()


def get_file_group(file_type):
    # Most common document types
    common_document_types = ['pdf', 'doc', 'docx', 'txt']

    # Other document types
    other_document_types = ['rtf', 'odt', 'latex', 'markdown', 'rst', 'md']

    # Spreadsheet types
    spreadsheet_types = ['xls', 'xlsx', 'xlsb', 'ods', 'csv']

    # Presentation types
    presentation_types = ['ppt', 'pptx', 'odp']

    # Image types
    image_types = ['bmp', 'gif', 'png', 'jpg', 'jpeg', 'tiff', 'svg', 'webp', 'ico', 'emf', 'wmf']

    # Audio types
    audio_types = ['mp3', 'wav', 'flac', 'ogg']

    # Video types
    video_types = ['mp4', 'webm']

    # Archive types
    archive_types = ['zip', 'rar', 'tar', 'gz', 'bz2', '7z', 'xz', 'cab', 'iso', 'dmg', 'xpi']

    # Programming languages
    programming_types = ['c', 'cpp', 'cs', 'java', 'py', 'js', 'php', 'rb', 'go', 'rs', 'scala', 'lisp', 'asm']

    # Web technologies
    web_types = ['html', 'css', 'js', 'json', 'xml', 'php']

    # Executable types
    executable_types = ['exe', 'dll', 'so', 'dex', 'apk', 'jar', 'elf', 'msi']

    # Configuration types
    config_types = ['ini', 'json', 'xml', 'yaml', 'toml']

    # Create a dictionary to map file types to groups
    file_groups = {
        'common_document': common_document_types,
        'document': other_document_types,
        'spreadsheet': spreadsheet_types,
        'presentation': presentation_types,
        'image': image_types,
        'audio': audio_types,
        'video': video_types,
        'archive': archive_types,
        'programming': programming_types,
        'web': web_types,
        'executable': executable_types,
        'configuration': config_types
    }

    # Convert input to lowercase for case-insensitive matching
    file_type = file_type.lower()

    # Check each group for the file type
    for group, types in file_groups.items():
        if file_type in types:
            return group

    # If no match is found, return 'unknown'
    return 'unknown'


def get_file_info(file_path):
    folder_full_path = os.path.dirname(os.path.abspath(file_path))
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    with open(file_path, 'rb') as f:
        file_bytes = f.read()

    file_type = magika.identify_bytes(file_bytes).output.ct_label

    file_data = {
        'folder_full_path': folder_full_path,
        'file_name': file_name,
        'file_full_path': os.path.abspath(file_path),
        'file_extension': file_extension,
        'last_accessed': datetime.fromtimestamp(os.path.getatime(file_path)),
        'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)),
        'created_time': datetime.fromtimestamp(os.path.getctime(file_path)),
        'file_size': os.path.getsize(file_path),
        'is_folder': os.path.isdir(file_path),
        'file_type': file_type,
        'file_group': get_file_group(file_type),
        'file_hash': sha256(file_bytes).hexdigest(),
    }

    return file_data
