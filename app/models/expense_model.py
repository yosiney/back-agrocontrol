from pydantic import BaseModel
from datetime import date
from typing import Optional

class Expense(BaseModel):
    date: str
    category: str
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    cost: float
