from typing import List, Optional, Union
from pydantic import BaseModel, Field
from typing_extensions import Literal


class DataField(BaseModel):
    roleid: int = Field(..., description="Role ID associated with the field, default is 1")
    object_name: str = Field(..., description="Name of the object, e.g., Account, Contact, Lead, Activity etc.")
    field_id: int = Field(..., description="Unique identifier for the field, e.g., 12345")
    name: str = Field(..., description="Label, DisplayName of the field, e.g., FirstName, LastName, Email etc.")
    FieldName: str = Field(..., description="API name of the field, e.g., First_Name__c, Last_Name__c, Email__c etc.")
    field_type: str = Field(..., description="Data type of the field, e.g., String, Number, Date etc.")


class Order(BaseModel):
    field: DataField
    direction: Literal["ASC", "DESC"]
    
    
class OutputSchema(BaseModel):
    object_name: str = Field(..., description="Name of the object, e.g., Account, Contact, Lead, Activity etc.")
    role_id: int = Field(..., description="Role ID associated with the output, default is 1")
    intent: str = Field(..., description="Intent of the Query, e.g., GET, SUMMARIZE, AGGREGATE, POST, UPDATE, DELETE")
    output_format: str = Field(..., description="Format of the output, e.g., TABLE, CARD, LIST, TEXT, SUMMARY")
    data_fields: List[DataField] = Field(..., description="List of data fields to include in the output")
    filters: Optional[List[DataField]] = Field(..., description="List of filters to apply to the output")
    limit: Union[int, str] = Field(1, description="Limit on the number of records to return e.g., 10, 100, 'ALL'")
    order: Order = Field(..., description="Ordering of the output records")
    groupBy: Optional[List[DataField]] = Field(..., description="List of fields to group the output by")
    
class AgentSchema(BaseModel):
    welcome_message: str = Field(..., description="Welcome message for the agent"),
    output_schemas: List[OutputSchema] = Field(..., description="List of output schemas for the agent")
    open_end_message: str = Field(..., description="Would you like to know about Open Leads, Opportunities or any other object?, etc.")