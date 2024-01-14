import json
from typing_extensions import Literal
from typing import Dict, Optional
from pydantic import BaseModel, constr, validator, ConstrainedStr
from com.platform.models.checkpoint_type_model import CheckpointType


class CheckpointModel(BaseModel):

    """Model which parse and validate user checpoint table value and defines proper structure"""
    
    process_id : constr(regex=r"^[1-9]\d*$", strip_whitespace=True)
    checkpoint_sequence : constr(regex=r"^[1-9]\d*$", strip_whitespace=True)
    process_name : constr(strip_whitespace=True)
    checkpoint_type : constr(strip_whitespace=True)
    script_type : Optional[Literal["FILE", "QUERY"]]
    script : Optional[constr(strip_whitespace=True)]
    source : Optional[constr(strip_whitespace=True)]
    target : Optional[constr(strip_whitespace=True)]
    configuration: Optional[Dict]
    is_active: bool


    @validator("checkpoint_type", pre=True)
    def format_checkpoint_type(cls, value: str):

        fmt_checkpoint: str = "_".join(value.strip().upper().split(" "))

        if fmt_checkpoint not in CheckpointType.__members__:
            raise ValueError(f"Invalid checkpoint_type: {fmt_checkpoint}, execution accepts only {CheckpointType.__members__}")
        
        return fmt_checkpoint if value else None
    

    @validator("script_type", pre=True)
    def format_script_type(cls, value: str):
        return value.strip().upper() if value else None


    @validator("source", "target", pre=True)
    def format_path(cls, value: str):        
        return value.strip().strip("/") if value else None


    @validator("configuration", pre=True)
    def format_configuration(cls, value: str):
        return json.loads(value) if value else None


    class Config:
        allow_mutation = False
