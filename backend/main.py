from fastapi import FastAPI, HTTPException
from .models import ComparisonRequest, ComparisonResponse, ComparisonResult
from .logic import get_stock_price_usd, calculate_financial_breakdown, calculate_alignment_score

app = FastAPI(
    title="Project C.O.D.E. API",
    description="API for comparing career offers.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "API is running."}

@app.post("/api/v1/compare", response_model=ComparisonResponse)
async def compare_offers(request: ComparisonRequest):
    """
    Accepts a list of offers and user preferences, then returns a
    full financial breakdown and alignment score for each.
    """
    results = []
    
    if not request.offers:
        raise HTTPException(status_code=400, detail="No offers provided for comparison.")

    for offer in request.offers:
        stock_price = get_stock_price_usd(offer.stock_ticker)
        if stock_price == 0.0:
            # Decide how to handle this. For MVP, we'll proceed but the RSU value will be 0.
            # A better version might raise an error.
            print(f"Warning: Could not fetch stock price for {offer.stock_ticker}. RSU value will be 0.")

        financials = calculate_financial_breakdown(offer, stock_price)
        
        score = calculate_alignment_score(financials, request.preferences)
        
        result = ComparisonResult(
            input_offer=offer,
            financials=financials,
            alignment_score=score
        )
        results.append(result)

    # Sort the results by the alignment score in descending order
    results.sort(key=lambda x: x.alignment_score, reverse=True)

    return ComparisonResponse(results=results)
