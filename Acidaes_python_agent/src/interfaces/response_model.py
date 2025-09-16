from pydantic import BaseModel
from typing import List, Any

class ResponseData(BaseModel):
    data: List[Any]

class ResponseModel(BaseModel):
    responseData: ResponseData
