from platform import system
from com.platform.constants.placeholders import Placeholder


class Helper:

    @staticmethod
    def is_linux():
        """Check the current system is linux"""
        return system() == "Linux"

    @staticmethod
    def singular_or_plural(value: int) -> str:
        """Used for defining words with singular or plural based on numbers"""
        return "s" if value > 1 else ""
    
    @staticmethod
    def strip_path(value: str) -> str:
        """Used for formatting GCS blob path"""
        return value.strip().strip("/")
    
    @staticmethod
    def extract_file_name(value: str) -> str:
        """Extract file name from complete file path"""
        return value.strip().split("/" if Helper.is_linux() else "\\")[-1]
    
    @staticmethod
    def format_log_name(prefix: int, suffix: str) -> str:
        return Placeholder.LOG_FILE_NAME.value.replace(Placeholder.PROCESS_ID.value, str(prefix)).replace(Placeholder.RUNTIME.value, suffix)
        