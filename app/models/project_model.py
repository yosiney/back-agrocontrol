from pydantic import BaseModel
from typing import Optional, Literal

class Project(BaseModel):
    name: str
    location: str
    status: Literal["activo", "terminado"] = "activo"
    planting_date: str  # "15 Mar 2025"
    harvest_date: Optional[str] = None  # "15 Nov 2025"  
    area: str  # "2.5 hectáreas"