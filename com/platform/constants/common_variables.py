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
    DATE: str = datetime.now().strftime("%Y-%m-%d")
    RUNTIME: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # GCP Project details
    PROJECT_ID: str      = "ultra-cinema-406217"
    PROJECT_DATASET: str = "pp_compliance_ods"

    # Bigquery Table Information
    REF_TABLE_NAME: str  = "reference"
    REF_LOG_TABLE_NAME: str  = "reference_log"
    CHK_TABLE_NAME: str  = "reference_checkpoint"
    CHK_LOG_TABLE_NAME: str  = "reference_checkpoint_log"

    REF_TABLE_IDN: str   = __table_identifier(PROJECT_ID, PROJECT_DATASET, REF_TABLE_NAME)
    CHK_TABLE_IDN: str   = __table_identifier(PROJECT_ID, PROJECT_DATASET, CHK_TABLE_NAME)
    REF_LOG_TABLE_IDN: str = __table_identifier(PROJECT_ID, PROJECT_DATASET, REF_LOG_TABLE_NAME)
    CHK_LOG_TABLE_IDN: str = __table_identifier(PROJECT_ID, PROJECT_DATASET, CHK_LOG_TABLE_NAME)

    # Colud Storage Information
    GCP_BUCKET_URL: str  = ""
    GCP_BUCKET_NAME: str = "platform_prod_bucket"

    GCP_LOG_DIR_NAME: str      = "log"
    GCP_SCRIPT_DIR_NAME: str   = "script"
    GCP_INBOUND_DIR_NAME: str  = "inbound"
    GCP_OUTBOUND_DIR_NAME: str = "outbound"
    GCP_MANDATORY_BLOBS: List[str] = [GCP_LOG_DIR_NAME, GCP_SCRIPT_DIR_NAME, GCP_INBOUND_DIR_NAME, GCP_OUTBOUND_DIR_NAME]



