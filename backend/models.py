from pydantic import BaseModel, Field
from typing import List, Optional

# --- Input Models (Data we receive from the frontend) ---

class OfferInput(BaseModel):
    """
    Represents the raw data for a single job offer, as entered by the user.
    """
    company_name: str = Field(..., description="Name of the company")
    stock_ticker: str = Field(..., description="Public stock ticker symbol, e.g., GOOGL")
    base_salary: float = Field(..., gt=0, description="Annual base salary in INR")
    bonus_percent: float = Field(..., ge=0, description="Target performance bonus as a percentage (e.g., 15 for 15%)")
    joining_bonus: float = Field(..., ge=0, description="One-time joining bonus in INR")
    rsu_grant_usd: float = Field(..., ge=0, description="Total value of RSU grant in USD over 4 years")

class UserPreferences(BaseModel):
    """
    Represents the user's personal weights for each decision criterion.
    """
    year_1_cash: int = Field(default=5, ge=1, le=10)
    four_year_value: int = Field(default=5, ge=1, le=10)
    # These will be manually rated by the user in the MVP
    work_life_balance: int = Field(default=5, ge=1, le=10)
    career_growth: int = Field(default=5, ge=1, le=10)

class ComparisonRequest(BaseModel):
    """
    The main request body for the /compare endpoint.
    """
    offers: List[OfferInput]
    preferences: UserPreferences


# --- Output Models (Data we send back to the frontend) ---

class FinancialBreakdown(BaseModel):
    """
    Calculated financial metrics for a single offer.
    """
    monthly_take_home: float
    year_1_total_comp: float
    four_year_average_comp: float
    total_rsu_value_inr: float

class ComparisonResult(BaseModel):
    """
    The complete, calculated result for a single offer, including its alignment score.
    """
    input_offer: OfferInput
    financials: FinancialBreakdown
    alignment_score: float

class ComparisonResponse(BaseModel):
    """
    The final response object sent back to the frontend.
    """
    results: List[ComparisonResult]
