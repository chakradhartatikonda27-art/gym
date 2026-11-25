from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ShiftOpenRequest(BaseModel):
    shift_name: str = "MORNING"
    opening_balance: Decimal = Field(default=Decimal("2000.00"), ge=0)

class ShiftCloseRequest(BaseModel):
    counted_cash: Decimal = Field(..., ge=0)
    closing_notes: Optional[str] = None
    shortage_justification: Optional[str] = None

class ShiftResponse(BaseModel):
    shift_id: str
    shift_name: str
    shift_status: str
    opening_balance: Decimal
    closing_cash_counted: Optional[Decimal] = None
    expected_cash_calculated: Optional[Decimal] = None
    discrepancy_amount: Optional[Decimal] = None
