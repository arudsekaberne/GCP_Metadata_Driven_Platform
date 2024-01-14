import json
from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel, constr, validator
from com.platform.constants.table_schema import CheckpointType, CheckpointScriptType


class CheckpointModel(BaseModel):

    """Model which parse and validate user checpoint table value and defines proper structure"""
    
    process_id : constr(regex=r"^[1-9]\d*$", strip_whitespace=True)
    checkpoint_sequence : constr(regex=r"^[1-9]\d*$", strip_whitespace=True)
    process_name : constr(strip_whitespace=True)
    checkpoint_type : constr(strip_whitespace=True)
    script_type : constr(strip_whitespace=True)
    script : Optional[constr(strip_whitespace=True)]
    source : Optional[constr(strip_whitespace=True)]
    target : Optional[constr(strip_whitespace=True)]
    configuration: Optional[Dict]
    is_active: bool
    last_modified_utc: datetime


    @validator("checkpoint_type", pre=True)
    def format_checkpoint_type(cls, value: str):

        fmt_checkpoint: str = "_".join(value.strip().upper().split(" "))

        if fmt_checkpoint not in CheckpointType.__members__:
            raise ValueError(f"Invalid checkpoint_type: {fmt_checkpoint}, execution accepts only {CheckpointType.__members__}")
        
        return fmt_checkpoint if value else None
    

    @validator("script_type", pre=True)
    def format_script_type(cls, value: str):

        fmt_script_type: str = value.strip().upper()

        if fmt_script_type not in CheckpointScriptType.__members__:
            raise ValueError(f"Invalid script_type: {fmt_script_type}, execution accepts only {CheckpointScriptType.__members__}")
        
        return value.strip().upper() if value else None


    @validator("source", "target", pre=True)
    def format_path(cls, value: str):        
        return value.strip().strip("/") if value else None


    @validator("configuration", pre=True)
    def parse_configuration(cls, value: str):

        if value:
            value_dict: Dict = json.loads(value)
            return value_dict
    
        return None


    class Config:
        allow_mutation = False
