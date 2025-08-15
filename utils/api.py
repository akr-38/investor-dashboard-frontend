# utils/api.py
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("BASE_URL not set in .env")

def fetch_registrations(category, manufacturer, start_year, start_quarter, end_year, end_quarter):
    """
    Calls the backend API based on dropdown selections and date range.
    Returns JSON response.
    """
    # Determine endpoint based on dropdown selections
    if category == "All Categories" and manufacturer == "All Manufacturers":
        endpoint = "/all_categories_all_manufacturers"
    elif category == "All Categories":
        endpoint = "/all_categories_specific_manufacturer"
    elif manufacturer == "All Manufacturers":
        endpoint = "/specific_category_all_manufacturers"
    else:
        endpoint = "/specific_category_specific_manufacturer"

    url = BASE_URL + endpoint

    payload = {
        "category": category if category != "All Categories" else "",
        "manufacturer": manufacturer if manufacturer != "All Manufacturers" else "",
        "start_year": start_year,
        "start_quarter": start_quarter,
        "end_year": end_year,
        "end_quarter": end_quarter
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
