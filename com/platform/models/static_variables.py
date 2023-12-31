from datetime import datetime
from pydantic import BaseModel


class StaticVariables(BaseModel):

    """Module which holds common static variables (only getter enabled)"""

    # Execution variables
    RUNTIME: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Execution file names
    LOG_FILE_NAME_PLACEHOLDER: str = r"{}_PLATFORM_{}.log"

    # Execution paths
    LOG_FILE_PATH: str = r"C:\Users\USER\OneDrive\Career\Projects\GCP_Metadata_Driven_Pipeline\log"

    class Config:
        frozen = True