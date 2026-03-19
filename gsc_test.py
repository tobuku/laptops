"""
Google Search Console - Connection Test
Property: FindLaptopDeals.com
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import date, timedelta

KEY_FILE = ".gsc-credentials/laptoplane-blogspot-autoposter-c7da82883623.json"
PROPERTY_URL = "sc-domain:findlaptopdeals.com"  # domain property format
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

def get_service():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    return build("searchconsole", "v1", credentials=creds)

def test_connection(service):
    print("=== Testing GSC Connection ===")
    sites = service.sites().list().execute()
    site_list = sites.get("siteEntry", [])
    if not site_list:
        print("WARNING: No sites returned. The service account may not have access yet.")
        return False
    print(f"Sites accessible ({len(site_list)}):")
    for site in site_list:
        print(f"  - {site['siteUrl']}  [{site['permissionLevel']}]")
    return True

def query_performance(service):
    print("\n=== Search Performance (last 28 days) ===")
    end = date.today() - timedelta(days=3)   # GSC data lags ~3 days
    start = end - timedelta(days=28)

    body = {
        "startDate": str(start),
        "endDate": str(end),
        "dimensions": ["query"],
        "rowLimit": 10
    }

    try:
        response = service.searchanalytics().query(siteUrl=PROPERTY_URL, body=body).execute()
        rows = response.get("rows", [])
        if not rows:
            print("No data returned. The property may use a different URL format (try with/without sc-domain:).")
            return
        print(f"Top {len(rows)} queries ({start} to {end}):\n")
        print(f"{'Query':<40} {'Clicks':>8} {'Impressions':>12} {'CTR':>8} {'Position':>10}")
        print("-" * 80)
        for row in rows:
            q = row["keys"][0]
            print(f"{q:<40} {row['clicks']:>8.0f} {row['impressions']:>12.0f} {row['ctr']:>7.1%} {row['position']:>10.1f}")
    except Exception as e:
        print(f"Error querying analytics: {e}")
        # Try with https:// prefix as fallback
        print("\nRetrying with https:// property format...")
        try:
            alt_url = "https://findlaptopdeals.com/"
            response = service.searchanalytics().query(siteUrl=alt_url, body=body).execute()
            rows = response.get("rows", [])
            if rows:
                print(f"Success with {alt_url}")
                print(f"Top {len(rows)} queries:\n")
                for row in rows:
                    q = row["keys"][0]
                    print(f"  {q}")
        except Exception as e2:
            print(f"Also failed: {e2}")

if __name__ == "__main__":
    service = get_service()
    connected = test_connection(service)
    if connected:
        query_performance(service)
    print("\nDone.")
