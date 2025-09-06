🚚 Real-Time Delivery Route Tracker

A Streamlit-based delivery tracking system that lets drivers manage parcel deliveries with optimized routes and allows customers to track their orders in real time — similar to apps like Swiggy or Zomato.

📂 Project Files

streamlit_delivery_app.py → Main Streamlit app

parcels_seed.csv → Demo parcel dataset (used to seed the system)

requirements.txt → Python dependencies

⚙️ System Prerequisites

Python 3.9+

pip (comes with Python)

[Optional] Google Maps API Key (for realistic route drawing)

[Optional] Twilio (if you want to enable SMS notifications)

🚀 Setup & Installation

Clone the repository

git clone https://github.com/riddhisr/riri_Real_Time_Delivery_Route_Tracker.git
cd riri_Real_Time_Delivery_Route_Tracker


Create & activate a virtual environment

python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows


Install dependencies

pip install -r requirements.txt


[Optional] Configure API Keys
Create a folder .streamlit and a file .streamlit/secrets.toml with your keys:

# Google Maps (optional, for real route visualization)
GOOGLE_MAPS_API_KEY = "your_api_key_here"

# Twilio (optional, for SMS updates)
TWILIO_ACCOUNT_SID = "your_sid_here"
TWILIO_AUTH_TOKEN = "your_token_here"
TWILIO_PHONE_NUMBER = "+91xxxxxxxxxx"


Run the app

streamlit run streamlit_delivery_app.py

📱 Features
👨‍✈️ Driver View

View assigned parcels (15–20 deliveries/day)

Get optimized delivery routes (Google Directions API if available, else fallback algorithm)

See delivery points and live progress on an interactive Folium map

👤 Customer View

Enter Parcel ID to track your delivery

View driver’s live location, estimated arrival, and route visualization

Get real-time updates as parcel moves through statuses: Placed → Warehouse → In Transit → Delivered

Provide feedback & rating after delivery

🛠 Notes

App uses parcels_seed.csv as demo data (simulating a database).

Without Google API, route optimization falls back to a simple nearest-neighbour approach.

Works fully offline for testing (with random driver movement).

Extendable to integrate with real databases & SMS/email notifications.

📸 Screenshots 

Driver dashboard with route map

Customer live tracking page

📌 Tech Stack

Frontend/Backend → Streamlit

Maps & Routes → Folium + Google Maps API (optional)

Data → CSV 

Extras → Twilio (optional SMS)
