"""
Amazon Product Image Fetcher for FindLaptopDeals.com
Uses Amazon Creators API (OAuth 2.0 / LWA) + PA API 5.0

USAGE:
  python amazon_images.py              # Fetch images and update HTML files
  python amazon_images.py --dry-run    # Preview without modifying any files
  python amazon_images.py --test-auth  # Test credentials only, no API calls

REQUIREMENTS:
  pip install requests python-dotenv

CREDENTIALS (stored in .env — never committed to git):
  AMAZON_ACCESS_KEY  = amzn1.application-oa2-client.xxx  (Client ID)
  AMAZON_SECRET_KEY  = amzn1.oa2-cs.v1.xxx               (Client Secret)
  AMAZON_ASSOCIATE_TAG = dwelldoc-20

NOTE:
  Amazon Creators API requires 10 qualifying sales in the past 30 days
  to access the PA API. If you get a 401/403, check your eligibility at
  associates.amazon.com under Reports > Earnings.
"""

import os
import json
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
CLIENT_ID     = os.getenv("AMAZON_ACCESS_KEY")
CLIENT_SECRET = os.getenv("AMAZON_SECRET_KEY")
ASSOCIATE_TAG = os.getenv("AMAZON_ASSOCIATE_TAG", "dwelldoc-20")

TOKEN_URL  = "https://api.amazon.com/auth/o2/token"
PA_API_URL = "https://webservices.amazon.com/paapi5/searchitems"

REPO_ROOT  = Path(__file__).parent
DATA_DIR   = REPO_ROOT / "data"
IMAGE_MAP_FILE = DATA_DIR / "product-images.json"

# --- Products ---
# h3 must exactly match the text inside <h3>...</h3> in the HTML file
PRODUCTS = [

    # ---- laptop-backpacks.html ----------------------------------------
    {
        "id":     "matein",
        "search": "Matein Travel Laptop Backpack",
        "file":   "laptop-backpacks.html",
        "h3":     "Matein Travel Laptop Backpack",
    },
    {
        "id":     "tzowla",
        "search": "Tzowla Business Laptop Backpack",
        "file":   "laptop-backpacks.html",
        "h3":     "Tzowla Business Laptop Backpack",
    },
    {
        "id":     "kopack",
        "search": "Kopack Slim Laptop Backpack Water Resistant Anti Theft",
        "file":   "laptop-backpacks.html",
        "h3":     "Kopack Slim Laptop Backpack - Water-Resistant Anti-Theft",
    },
    {
        "id":     "pacsafe",
        "search": "Pacsafe Venturesafe EXP45 Anti Theft Travel Backpack",
        "file":   "laptop-backpacks.html",
        "h3":     "Pacsafe Venturesafe EXP45 Anti-Theft Travel Backpack",
    },
    {
        "id":     "bopai",
        "search": "Bopai Anti Theft Laptop Backpack USB Charging",
        "file":   "laptop-backpacks.html",
        "h3":     "Bopai Anti-Theft Laptop Backpack with USB Charging",
    },
    {
        "id":     "ambor",
        "search": "Ambor Laptop Backpack Women Professional Slim",
        "file":   "laptop-backpacks.html",
        "h3":     "Ambor Laptop Backpack for Women - Professional Slim Design",
    },
    {
        "id":     "yorepek",
        "search": "Yorepek Extra Large Travel Laptop Backpack 35L",
        "file":   "laptop-backpacks.html",
        "h3":     "Yorepek Extra Large Travel Laptop Backpack",
    },
    {
        "id":     "swissgear",
        "search": "SwissGear 1900 ScanSmart Laptop Backpack",
        "file":   "laptop-backpacks.html",
        "h3":     "SwissGear 1900 ScanSmart Laptop Backpack",
    },
    {
        "id":     "shrradoo",
        "search": "Shrradoo Extra Large 52L Travel Laptop Backpack TSA",
        "file":   "laptop-backpacks.html",
        "h3":     "Shrradoo Extra Large 52L Travel Laptop Backpack",
    },
    {
        "id":     "matein-usb",
        "search": "Matein Travel Laptop Backpack USB charging port",
        "file":   "laptop-backpacks.html",
        "h3":     "Matein Travel Laptop Backpack (USB Edition)",
    },
    {
        "id":     "tzowla-usb",
        "search": "Tzowla Business Laptop Backpack USB Headphone Port",
        "file":   "laptop-backpacks.html",
        # HTML entity for & must match exactly what's in the file
        "h3":     "Tzowla Business Laptop Backpack with USB &amp; Headphone Port",
    },

    # ---- portable-power-banks.html ------------------------------------
    {
        "id":     "iniu-10000",
        "search": "INIU Portable Charger 10000mAh Slim Power Bank",
        "file":   "portable-power-banks.html",
        "h3":     "INIU Portable Charger, 10,000mAh Slim Power Bank",
    },
    {
        "id":     "anker-20100",
        "search": "Anker PowerCore 20100 Portable Charger",
        "file":   "portable-power-banks.html",
        "h3":     "Anker PowerCore 20100 Portable Charger",
    },
    {
        "id":     "anker-26800",
        "search": "Anker PowerCore+ 26800 PD Portable Charger USB-C",
        "file":   "portable-power-banks.html",
        "h3":     "Anker PowerCore+ 26800 PD Portable Charger with USB-C",
    },
    {
        "id":     "baseus-30000",
        "search": "Baseus Power Bank 30000mAh 65W PD Fast Charging",
        "file":   "portable-power-banks.html",
        "h3":     "Baseus Power Bank 30,000mAh, 65W PD Fast Charging",
    },
    {
        "id":     "charmast",
        "search": "Charmast Ultra Slim Portable Charger 10000mAh",
        "file":   "portable-power-banks.html",
        "h3":     "Charmast Ultra Slim Portable Charger, 10,000mAh",
    },
    {
        "id":     "miady",
        "search": "Miady 10000mAh Dual USB Portable Charger 2 Pack",
        "file":   "portable-power-banks.html",
        "h3":     "Miady 10,000mAh Dual USB Portable Charger (2-Pack)",
    },
    {
        "id":     "anker-325",
        "search": "Anker 325 Power Bank PowerCore 20000",
        "file":   "portable-power-banks.html",
        "h3":     "Anker 325 Power Bank (PowerCore 20K)",
    },
    {
        "id":     "iniu-20000",
        "search": "INIU Power Bank 20000mAh 65W PD Fast Charge",
        "file":   "portable-power-banks.html",
        "h3":     "INIU Power Bank 20,000mAh, 65W PD Fast Charge",
    },
]

# CSS added to both HTML files to style the injected images
IMAGE_CSS = """\
    /* Product images (injected by amazon_images.py) */
    .product-img-wrap { text-align: center; margin: 0 0 16px; }
    .product-img-wrap img { max-height: 180px; max-width: 200px; object-fit: contain; border-radius: 4px; }
"""


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def get_token():
    """Obtain an OAuth 2.0 access token from Amazon LWA."""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("AMAZON_ACCESS_KEY and AMAZON_SECRET_KEY must be set in .env")

    resp = requests.post(TOKEN_URL, data={
        "grant_type":    "client_credentials",
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }, timeout=10)

    if resp.status_code != 200:
        raise RuntimeError(
            f"Auth failed ({resp.status_code}): {resp.text}\n"
            "Check your credentials in .env. If you see a 401, your account may not\n"
            "yet have 10 qualifying sales in the past 30 days."
        )

    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError(f"No access_token in response: {resp.text}")
    return token


# ---------------------------------------------------------------------------
# PA API
# ---------------------------------------------------------------------------

def search_product(token, search_term):
    """Search PA API for a product and return the primary large image URL."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    }
    payload = {
        "Keywords":    search_term,
        "Resources":   ["Images.Primary.Large", "ItemInfo.Title"],
        "SearchIndex": "All",
        "ItemCount":   1,
        "PartnerTag":  ASSOCIATE_TAG,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.com",
    }

    resp = requests.post(PA_API_URL, json=payload, headers=headers, timeout=15)

    if resp.status_code == 401:
        raise RuntimeError(
            "PA API returned 401. Your account likely needs 10 qualifying sales "
            "in the past 30 days to access the PA API via Creators API."
        )
    if resp.status_code != 200:
        raise RuntimeError(f"PA API error ({resp.status_code}): {resp.text}")

    data  = resp.json()
    items = data.get("SearchResult", {}).get("Items", [])
    if not items:
        return None

    return items[0].get("Images", {}).get("Primary", {}).get("Large", {}).get("URL")


# ---------------------------------------------------------------------------
# HTML injection
# ---------------------------------------------------------------------------

def add_image_css(html, css):
    """Inject image CSS into the <style> block (once per file)."""
    if "product-img-wrap" in html:
        return html  # already added
    return html.replace("  </style>", css + "  </style>", 1)


def inject_image(html, h3_text, img_url, product_id):
    """
    Insert a product image div at the top of the matching product card.
    Finds the product-card div that contains h3_text, then inserts the
    image block immediately after the opening div tag.
    """
    marker = f'id="img-{product_id}"'
    if marker in html:
        return html  # already injected, skip

    # Find the h3
    h3_tag = f"<h3>{h3_text}</h3>"
    h3_pos = html.find(h3_tag)
    if h3_pos == -1:
        print(f"    WARNING: Could not find <h3>{h3_text[:40]}</h3> — skipping")
        return html

    # Walk back to find the opening product-card div
    card_pos = html.rfind('<div class="product-card', 0, h3_pos)
    if card_pos == -1:
        print(f"    WARNING: Could not find product-card for: {h3_text[:40]} — skipping")
        return html

    # End of the opening tag (past the >)
    tag_end = html.index(">", card_pos) + 1

    img_block = (
        f'\n    <div class="product-img-wrap">'
        f'<img src="{img_url}" alt="{h3_text}" loading="lazy" {marker}>'
        f'</div>'
    )

    return html[:tag_end] + img_block + html[tag_end:]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(dry_run=False, test_auth=False):
    print("Amazon Product Image Fetcher — FindLaptopDeals.com")
    print("=" * 52)

    # Validate credentials are present
    if not CLIENT_ID or not CLIENT_SECRET:
        print("\nERROR: Missing credentials. Check your .env file.")
        return

    # Auth
    print("\nStep 1: Authenticating with Amazon LWA...")
    try:
        token = get_token()
        print("  OK — access token obtained")
    except Exception as e:
        print(f"\n  FAILED: {e}")
        return

    if test_auth:
        print("\nCredentials are valid. Run without --test-auth to fetch images.")
        return

    # Load HTML files into memory
    html_files = {}
    for p in PRODUCTS:
        fname = p["file"]
        if fname not in html_files:
            path = REPO_ROOT / fname
            if not path.exists():
                print(f"\nERROR: {fname} not found at {path}")
                return
            html_files[fname] = path.read_text(encoding="utf-8")

    # Fetch images
    print(f"\nStep 2: Fetching images for {len(PRODUCTS)} products...")
    image_map = {}
    errors = []

    for p in PRODUCTS:
        pid = p["id"]
        print(f"  [{pid}] {p['search'][:50]}...")
        try:
            url = search_product(token, p["search"])
            if url:
                image_map[pid] = url
                print(f"    Found: {url[:70]}")
            else:
                print(f"    No results returned — skipping")
                errors.append(pid)
        except RuntimeError as e:
            print(f"    ERROR: {e}")
            errors.append(pid)
            if "401" in str(e):
                print("\n  Stopping — PA API access denied. Check eligibility.")
                break

    if not image_map:
        print("\nNo images fetched. Nothing to update.")
        return

    # Save image map
    if not dry_run:
        DATA_DIR.mkdir(exist_ok=True)
        IMAGE_MAP_FILE.write_text(json.dumps(image_map, indent=2))
        print(f"\nImage map saved: data/product-images.json ({len(image_map)} entries)")

    # Inject images into HTML
    print(f"\nStep 3: Injecting images into HTML files...")
    for p in PRODUCTS:
        pid = p["id"]
        if pid not in image_map:
            continue
        fname  = p["file"]
        html   = html_files[fname]
        html   = add_image_css(html, IMAGE_CSS)
        html   = inject_image(html, p["h3"], image_map[pid], pid)
        html_files[fname] = html
        print(f"  Injected: {p['h3'][:55]}")

    # Write updated HTML files
    if not dry_run:
        for fname, html in html_files.items():
            (REPO_ROOT / fname).write_text(html, encoding="utf-8")
            print(f"\nWritten: {fname}")
        print("\nDone. Next steps:")
        print("  git add laptop-backpacks.html portable-power-banks.html data/product-images.json")
        print("  git commit -m 'Add Amazon product images to guide pages'")
        print("  git push")
    else:
        print(f"\nDry run complete — {len(image_map)} images found, no files modified.")

    if errors:
        print(f"\nSkipped {len(errors)} products: {errors}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Amazon product images for FindLaptopDeals.com")
    parser.add_argument("--dry-run",   action="store_true", help="Preview without writing any files")
    parser.add_argument("--test-auth", action="store_true", help="Test credentials only")
    args = parser.parse_args()
    main(dry_run=args.dry_run, test_auth=args.test_auth)
