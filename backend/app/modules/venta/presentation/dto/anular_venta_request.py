from uuid import UUID
from pydantic import BaseModel, Field

class AnularVentaRequest(BaseModel):
    supervisor_id: UUID = Field(..., description="UUID of the supervisor authorizing the annulment")
    reason: str = Field(..., max_length=300, description="Reason for the annulment")
