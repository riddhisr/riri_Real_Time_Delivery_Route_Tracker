Delivery App - Full Streamlit Demo

Files:
- streamlit_delivery_app.py
- parcels_seed.csv
- requirements.txt

System prerequisites:
- Python 3.9+
- libzbar (for barcode decoding):
  - Ubuntu/Debian: sudo apt-get install libzbar0
  - macOS (Homebrew): brew install zbar
  - Windows: use precompiled wheels for pyzbar or follow pyzbar docs

Setup:
1. Create & activate a venv:
   python -m venv venv
   source venv/bin/activate   (Linux/Mac)
   venv\Scripts\activate      (Windows)

2. Install python packages:
   pip install -r requirements.txt

3. Optionally set Streamlit secrets for Google Maps & Twilio:
   Create folder .streamlit and file .streamlit/secrets.toml with keys:

   # optional - Google Directions & Maps
   GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

   # optional - Twilio to send SMS (if you want real SMS)
   TWILIO_ACCOUNT_SID = "..."
   TWILIO_AUTH_TOKEN = "..."
   TWILIO_PHONE_NUMBER = "+91..."

4. Run the app:
   streamlit run streamlit_delivery_app.py

Notes:
- The app seeds an SQLite DB (parcels.db) from parcels_seed.csv on first run.
- If Google API key is provided, route optimization will use Directions API. Without it, a greedy nearest-neighbour algorithm is used.
- Camera QR scanning requires streamlit-camera-input and libzbar. If camera/scanning isn't available, use manual parcel selection.
