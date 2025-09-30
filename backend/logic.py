import yfinance as yf
from models import OfferInput, UserPreferences, FinancialBreakdown, ComparisonResult

# --- Constants ---
# This is a very rough approximation for simplicity. A real app would be more complex.
# Based on New Tax Regime for FY 2023-24, assuming salary > 15LPA.
FLAT_TAX_RATE = 0.30
STANDARD_DEDUCTION = 50000
# Professional tax and PF can be added for more accuracy, but let's keep it simple for MVP.
USD_TO_INR_RATE = 83.0  # We'll use a fixed rate for the MVP to avoid another API call

# --- Helper Functions ---

def get_stock_price_usd(ticker: str) -> float:
    """Fetches the current stock price for a given ticker from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        # 'regularMarketPrice' is a common field, 'currentPrice' is another
        price = stock.info.get('regularMarketPrice') or stock.info.get('currentPrice')
        if price is None:
            # Fallback for tickers that might not have regular market price (e.g., indices)
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
            else:
                return 0.0 # Could not find price
        return float(price)
    except Exception as e:
        print(f"Error fetching stock price for {ticker}: {e}")
        return 0.0 # Return 0 or handle error appropriately

# --- Core Calculation Functions ---

def calculate_financial_breakdown(offer: OfferInput, stock_price_usd: float) -> FinancialBreakdown:
    """Calculates all key financial metrics for a single offer."""
    
    # RSU Calculations
    total_rsu_value_inr = offer.rsu_grant_usd * USD_TO_INR_RATE
    yearly_rsu_inr = total_rsu_value_inr / 4

    # Taxable Income Calculation
    taxable_income = offer.base_salary - STANDARD_DEDUCTION
    total_tax = taxable_income * FLAT_TAX_RATE
    yearly_take_home_from_salary = offer.base_salary - total_tax

    # Total Compensation Calculations
    year_1_bonus = offer.base_salary * (offer.bonus_percent / 100)
    year_1_total_comp = yearly_take_home_from_salary + offer.joining_bonus + year_1_bonus + yearly_rsu_inr
    
    four_year_total_comp = (yearly_take_home_from_salary * 4) + offer.joining_bonus + (year_1_bonus * 4) + total_rsu_value_inr
    
    return FinancialBreakdown(
        monthly_take_home=round(yearly_take_home_from_salary / 12),
        year_1_total_comp=round(year_1_total_comp),
        four_year_average_comp=round(four_year_total_comp / 4),
        total_rsu_value_inr=round(total_rsu_value_inr)
    )

def calculate_alignment_score(financials: FinancialBreakdown, preferences: UserPreferences) -> float:
    """Calculates a personalized alignment score based on user weights."""
    # We need to normalize our financial values to a 1-10 scale to compare them with subjective scores.
    # This is a simple normalization. A more advanced version would normalize against the *other offers*.
    # For now, let's just use the raw values multiplied by weights as a simple score.
    
    score = (
        (financials.year_1_total_comp / 100000) * preferences.year_1_cash +
        (financials.four_year_average_comp / 100000) * preferences.four_year_value
    )
    # In the future, we would add the WLB and Career Growth scores here.
    
    return round(score, 2)
