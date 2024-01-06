from typing import Optional
from datetime import datetime
from pydantic import BaseModel, constr, validator


class InputModel(BaseModel):

    """Model which parse and validate user inputs and defines proper structure"""

    process_id      : constr(regex=r"^[1-9]\d*$", strip_whitespace=True)
    batch_date      : constr(regex=r"\d{4}-\d{2}-\d{2}", strip_whitespace=True)
    from_checkpoint : constr(regex=r"^[1-9]\d*$", strip_whitespace=True)
    to_checkpoint   : Optional[constr(regex=r"^[1-9]\d*$", strip_whitespace=True)]


    @validator("batch_date")
    def validate_date(cls, value: str):

        """This validates the batch date passed is in expected format 'YYYY-MM-DD'"""

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise ValueError("Invalid batch date format. Use YYYY-MM-DD.")
        
    
    @staticmethod
    def validate_id(id: str):

        """Function validates the given input id is greater than or equals 1"""

        clean_id: str  = id.strip()

        if int(clean_id) < 1:
            raise Exception("The input 'id' string does not match regex '^[1-9]\d*$'")
        return clean_id  

    class Config:
        allow_mutation = False
