import os
import shutil
from typing import Dict, Any
from .base_action import Action
from ..utils.logger import logger


class MoveAction(Action):
    def __init__(self, destination: str):
        self.destination = destination

    def execute(self, file_data: Dict[str, Any]) -> str:
        try:
            source_path = file_data['file_full_path']
            folder_full_path = file_data['folder_full_path']
            file_name = file_data['file_name'] + file_data['file_extension']
            destination_path = os.path.join(folder_full_path, self.destination, file_name)

            # Create the destination directory if it doesn't exist
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            # Move the file
            shutil.move(source_path, destination_path)

            logger.info(f"Moved file '{file_name}' to '{self.destination}'")
            return f"Moved to {self.destination}"
        except Exception as e:
            error_msg = f"Error moving file '{file_data['file_name']}': {str(e)}"
            logger.error(error_msg)
            return error_msg