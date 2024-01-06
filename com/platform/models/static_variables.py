from datetime import datetime
from com.platform.models.immutable_class import ImmutableMetaclass


class StaticVariables(metaclass=ImmutableMetaclass):

    """Immutable module which holds static variables (only getter enabled)"""

    # Restrict new variable creation and modification
    def __setattr__(self, name, value):
        raise AttributeError("Cannot create or set class or instance attribute '{}'".format(name))

    # Execution variables
    RUNTIME: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Project details
    PROJECT_ID: str       = "ultra-cinema-406217"
    PROJECT_DATASET: str  = "pp_compliance_ods"
    REFERENCE_TABLE: str  = "platform_reference"
    CHECKPOINT_TABLE: str = "platform_checkpoint"
    
    REFERENCE_TABLE_IDENTIFIER: str  = "`{}.{}.{}`".format(PROJECT_ID, PROJECT_DATASET, REFERENCE_TABLE)
    CHECKPOINT_TABLE_IDENTIFIER: str = "`{}.{}.{}`".format(PROJECT_ID, PROJECT_DATASET, CHECKPOINT_TABLE)

    # Execution file names
    LOG_FILE_NAME_PLACEHOLDER: str = r"{}_PLATFORM_{}.log"

    # Execution paths
    LOG_FILE_PATH: str = r"C:\Users\USER\OneDrive\Career\Projects\GCP_Metadata_Driven_Pipeline\log"
