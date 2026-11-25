from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date
from enum import Enum

class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class FastOnboardRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\+91[6-9]\d{9}$", example="+919849012345")
    full_name: str = Field(..., min_length=2, max_length=100, example="Arjun Kapoor")
    gender: GenderEnum
    date_of_birth: Optional[date] = None
    emergency_contact_phone: Optional[str] = None
    has_medical_conditions: bool = False
    medical_notes: Optional[str] = None
    waiver_signed: bool = True
    
    # Subscription
    plan_id: str
    start_date: date = Field(default_factory=date.today)
    
    # Payment Split
    cash_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    online_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    online_reference_id: Optional[str] = None
    cash_register_id: Optional[str] = None

class FastOnboardResponse(BaseModel):
    member_id: str
    member_code: str
    full_name: str
    subscription_id: str
    invoice_id: str
    invoice_number: str
    total_amount: Decimal
    paid_amount: Decimal
    balance_due: Decimal
    message: str
