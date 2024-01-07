import re
from typing import List
from datetime import datetime
from pydantic import BaseModel, constr, validator, Field
from com.platform.constants.common_variables import CommonVariables


class ReferenceModel(BaseModel):

    """Model which parse and validate user reference table value and defines proper structure"""
    
    id : constr(regex=r"^[1-9]\d*$", strip_whitespace=True)
    name : constr(strip_whitespace=True)
    project_folder : constr(strip_whitespace=True)
    alert_mail_ids: List[str]
    sla_days: int = Field(gt=0)
    log_retention_count: int = Field(gt=0)
    last_modified_utc: datetime
    is_active: bool
    is_live: bool


    @validator("project_folder", pre=True)
    def format_project_folder(cls, value: str):

        """This validate and format the project folder name"""
        
        return value.strip().strip("/")
    
    @validator("alert_mail_ids", pre=True)
    def validate_emails(cls, value: str):

        """This validates the alert mail ids passed is in expected format"""

        EMAIL_FORMAT: str = r'\b[A-Za-z0-9._%+-]+@gmail\.com\b'

        formatted_emails = [email.strip() for email in value.split(",")]
        for email in formatted_emails:
            if not re.match(EMAIL_FORMAT, email):
                raise ValueError(f"Invalid gmail address mentioned in alert_mail_ids, please check {CommonVariables.REF_TABLE_NAME} table. Also, make sure you used ',' as delimiter to mention multiple email ids.")

        return formatted_emails
    

    class Config:
        allow_mutation = False
