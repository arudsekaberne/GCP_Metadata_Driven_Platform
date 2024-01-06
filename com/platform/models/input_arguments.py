from typing import Optional
from datetime import datetime
from typing_extensions import Literal
from pydantic import BaseModel, Field, constr, validator


class InputArguments(BaseModel):

    """Model which parse and validate user inputs and defines proper structure"""

    process_id      : int = Field(ge=100)
    batch_date      : constr(regex=r"\d{4}-\d{2}-\d{2}", strip_whitespace=True)
    from_checkpoint : int = Field(ge=1)
    to_checkpoint   : Optional[int] = Field(ge=1)

    @validator("batch_date")
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise ValueError("Invalid batch date format. Use YYYY-MM-DD.")

    
