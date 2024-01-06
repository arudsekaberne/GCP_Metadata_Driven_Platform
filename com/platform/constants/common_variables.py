from typing import List
from datetime import datetime
from com.platform.models.immutable_model import ImmutableMetaModel


class CommonVariables(metaclass=ImmutableMetaModel):

    """Immutable module which holds common variables (only getter enabled)"""

    # Restrict new variable creation and modification
    def __setattr__(self, name, value):
        raise AttributeError(f"Cannot create or set class or instance attribute '{name}'")

    
    # Helpers
    __table_identifier     = lambda id, dataset, table: f"`{id}.{dataset}.{table}`"

    # Execution variables
    RUNTIME: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # GCP Project details
    PROJECT_ID: str      = "ultra-cinema-406217"
    PROJECT_DATASET: str = "pp_compliance_ods"

    # Bigquery Table Information
    REF_TABLE_NAME: str  = "platform_reference"
    CHK_TABLE_NAME: str  = "platform_checkpoint"
    REF_TABLE_IDN: str   = __table_identifier(PROJECT_ID, PROJECT_DATASET, REF_TABLE_NAME)
    CHK_TABLE_IDN: str   = __table_identifier(PROJECT_ID, PROJECT_DATASET, CHK_TABLE_NAME)

    # Colud Storage Information
    BUCKET_URL: str = ""
    BUCKET_NAME: str = "platform_prod_bucket"
    MANDATORY_BLOBS: List[str] = ["log", "script", "inbound", "outbound"]

    # Execution file names
    LOG_FILE_NAME_PLACEHOLDER: str = r"{}_PLATFORM_{}.log"

    # Execution paths
    LOG_FILE_PATH: str = r"C:\Users\USER\OneDrive\Career\Projects\GCP_Metadata_Driven_Pipeline\log"
