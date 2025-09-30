import time # <--- IMPORT THIS
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ComparisonRequest, ComparisonResponse, ComparisonResult
from .logic import get_stock_price_usd, calculate_financial_breakdown, calculate_alignment_score

app = FastAPI(
    title="Project C.O.D.E. API",
    description="API for comparing career offers.",
    version="1.0.0"
)

# Your robust CORS configuration
origins = [
    "https://project-code.streamlit.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https://.*\.cloudspaces\.litng\.ai|http://localhost:[0-9]+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    start_time = time.time() # <--- START TIMER
    print("[TIMING] --- Request received. Starting processing. ---")

    results = []
    
    if not request.offers:
        raise HTTPException(status_code=400, detail="No offers provided for comparison.")

    for offer in request.offers:
        yf_start_time = time.time() # <--- Start yfinance timer
        stock_price = get_stock_price_usd(offer.stock_ticker)
        yf_end_time = time.time() # <--- End yfinance timer
        yf_duration = yf_end_time - yf_start_time
        print(f"[TIMING] yfinance call for {offer.stock_ticker} took: {yf_duration:.2f} seconds")

        if stock_price == 0.0:
            print(f"Warning: Could not fetch stock price for {offer.stock_ticker}. RSU value will be 0.")
        
        financials = calculate_financial_breakdown(offer, stock_price)
        score = calculate_alignment_score(financials, request.preferences)
        
        result = ComparisonResult(
            input_offer=offer,
            financials=financials,
            alignment_score=score
        )
        results.append(result)

    results.sort(key=lambda x: x.alignment_score, reverse=True)

    end_time = time.time() # <--- END TIMER
    total_duration = end_time - start_time
    print(f"[TIMING] --- Total processing time inside API: {total_duration:.2f} seconds ---")

    return ComparisonResponse(results=results)
