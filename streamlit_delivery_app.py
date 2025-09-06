# import os
# import pandas as pd
# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# from dotenv import load_dotenv
# import requests
# import polyline
# from datetime import datetime, timedelta
# import random

# # ---------------------------
# # Load environment variables
# # ---------------------------
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# # ---------------------------
# # Load parcels CSV
# # ---------------------------
# @st.cache_data
# def load_data():
#     return pd.read_csv("parcels_seed.csv")

# df = load_data()

# # ---------------------------
# # Save updated CSV
# # ---------------------------
# def save_data(df):
#     df.to_csv("parcels_demo.csv", index=False)

# # ---------------------------
# # Streamlit Page Config
# # ---------------------------
# st.set_page_config(page_title="Delivery App Demo", layout="wide")
# st.title("🚚 Delivery App Demo")

# # ---------------------------
# # Role Selection
# # ---------------------------
# role = st.sidebar.selectbox("Login as", ["Customer", "Driver"])

# # ---------------------------
# # Helper: Google Maps Route
# # ---------------------------
# def get_google_route(origin, destination, waypoints=None):
#     url = "https://maps.googleapis.com/maps/api/directions/json"
#     params = {
#         "origin": origin,
#         "destination": destination,
#         "waypoints": waypoints,
#         "optimizeWaypoints": "true",
#         "key": GOOGLE_API_KEY
#     }
#     response = requests.get(url, params=params)
#     return response.json()

# # ---------------------------
# # Notifications (Demo)
# # ---------------------------
# def send_sms(phone, message):
#     # Demo: just print message
#     print(f"SMS to {phone}: {message}")

# # ---------------------------
# # CUSTOMER VIEW
# # ---------------------------
# # ---------------------------
# # CUSTOMER VIEW
# # ---------------------------
# import time

# if role == "Customer":
#     st.header("Track Your Parcel")

#     parcel_id_input = st.text_input("Enter Parcel ID")
#     track_button = st.button("Track Parcel")

#     if "tracking_parcel" not in st.session_state:
#         st.session_state.tracking_parcel = None

#     if track_button and parcel_id_input:
#         if parcel_id_input in df["parcel_id"].values:
#             st.session_state.tracking_parcel = parcel_id_input
#         else:
#             st.error("❌ Parcel not found!")
#             st.session_state.tracking_parcel = None

#     if st.session_state.tracking_parcel:
#         parcel = df[df["parcel_id"] == st.session_state.tracking_parcel].iloc[0]

#         # Ensure status is string
#         status = str(parcel["status"]).strip().lower()

#         if status == "placed":
#             st.info(f"📦 Your order has been placed, {parcel['customer_name']}!")

#         elif status == "warehouse":
#             st.info(f"🏢 Your order has reached the warehouse, {parcel['customer_name']}!")

#         elif status in ["out_for_delivery", "in_transit"]:
#             # Inject JS for auto-refresh every 30s
#             refresh_script = """
#             <script>
#             setTimeout(function(){
#                 window.location.reload();
#             }, 30000);
#             </script>
#             """
#             st.markdown(refresh_script, unsafe_allow_html=True)

#             # Initialize driver state
#             if "driver_lat" not in st.session_state or "driver_lon" not in st.session_state:
#                 st.session_state.driver_lat = float(parcel["lat"])
#                 st.session_state.driver_lon = float(parcel["lon"])
#                 st.session_state.last_update = time.time()

#             # Update location only every 30s
#             if time.time() - st.session_state.last_update > 30:
#                 st.session_state.driver_lat += random.uniform(-0.01, 0.01)
#                 st.session_state.driver_lon += random.uniform(-0.01, 0.01)
#                 st.session_state.last_update = time.time()

#             driver_lat = st.session_state.driver_lat
#             driver_lon = st.session_state.driver_lon
#             eta_minutes = random.randint(10, 15)

#             st.warning(f"🚚 {parcel['customer_name']}, your parcel {parcel['parcel_id']} is on the way!")
#             st.info(f"Driver location: ({driver_lat:.4f}, {driver_lon:.4f}) | ETA: {eta_minutes} minutes")

#             # Show map
#             m = folium.Map(location=[parcel["lat"], parcel["lon"]], zoom_start=12)
#             folium.Marker([driver_lat, driver_lon], popup="Driver is here", icon=folium.Icon(color="green")).add_to(m)
#             folium.Marker([parcel["lat"], parcel["lon"]], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
#             st_folium(m, width=700, height=500)

#         elif status == "delivered":
#             st.success(f"✅ {parcel['customer_name']}, your parcel {parcel['parcel_id']} has been delivered!")
#             st.subheader("📝 Give Feedback")
#             feedback = st.text_area("Write your feedback")
#             rating = st.slider("Rate your delivery experience", 1, 5, 5)
#             if st.button("Submit Feedback"):
#                 st.success("Thanks for your feedback!")

# # ---------------------------
# # DRIVER VIEW
# # ---------------------------
# elif role == "Driver":
#     st.header("Driver Dashboard")
#     driver_id = st.selectbox("Select Your Driver ID", df["driver_id"].unique())
#     driver_parcels = df[df["driver_id"] == driver_id]

#     st.subheader("Your Assigned Parcels")
#     st.dataframe(driver_parcels[["parcel_id","customer_name","address","status"]])

#     st.subheader("Start Delivery (QR Scan Simulation)")
#     parcel_to_deliver = st.selectbox("Select Parcel", driver_parcels["parcel_id"])

#     if "active_parcel" not in st.session_state:
#         st.session_state.active_parcel = None

#     if st.button("Start Delivery"):
#         st.session_state.active_parcel = parcel_to_deliver
#         df.loc[df["parcel_id"] == parcel_to_deliver, "status"] = "out_for_delivery"
#         df.loc[df["parcel_id"] == parcel_to_deliver, "start_time"] = datetime.now()
#         save_data(df)

#         parcel = df[df["parcel_id"] == parcel_to_deliver].iloc[0]
#         send_sms(parcel["phone"], f"Hello {parcel['customer_name']}, your parcel {parcel_to_deliver} is out for delivery! ETA approx 10-15 mins")

#         st.success(f"Started delivery for {parcel_to_deliver}. Notification sent!")

#     # Show route map for active parcel
#     if st.session_state.active_parcel:
#         parcel = df[df["parcel_id"] == st.session_state.active_parcel].iloc[0]
#         origin = "19.0760,72.8777"  # warehouse
#         destination = f"{parcel['lat']},{parcel['lon']}"
#         route_data = get_google_route(origin, destination)
#         if route_data.get("status") == "OK":
#             coords = polyline.decode(route_data["routes"][0]["overview_polyline"]["points"])
#             m = folium.Map(location=[parcel["lat"], parcel["lon"]], zoom_start=12)
#             folium.PolyLine(coords, color="blue", weight=4, opacity=0.7).add_to(m)
#             folium.Marker([parcel["lat"], parcel["lon"]], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
#             st_folium(m, width=700, height=500)
#         else:
#             # fallback map if route fails
#             m = folium.Map(location=[parcel["lat"], parcel["lon"]], zoom_start=12)
#             folium.Marker([parcel["lat"], parcel["lon"]], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
#             st_folium(m, width=700, height=500)

#     if st.button("Mark as Delivered"):
#         if st.session_state.active_parcel:
#             df.loc[df["parcel_id"] == st.session_state.active_parcel, "status"] = "delivered"
#             save_data(df)
#             parcel = df[df["parcel_id"] == st.session_state.active_parcel].iloc[0]
#             send_sms(parcel["phone"], f"✅ {parcel['customer_name']}, your parcel {parcel['parcel_id']} has been delivered!")
#             st.success(f"{st.session_state.active_parcel} marked as delivered. Waiting for customer confirmation...")
#             st.session_state.active_parcel = None


#-----


import os
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv
import requests
import polyline
from datetime import datetime
import random
import time

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# ---------------------------
# Load parcels CSV
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("parcels_seed.csv")

df = load_data()

# ---------------------------
# Save updated CSV
# ---------------------------
def save_data(df):
    df.to_csv("parcels_demo.csv", index=False)

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(page_title="Delivery App Demo", layout="wide")
st.title("🚚 Delivery App Demo")

# ---------------------------
# Role Selection
# ---------------------------
role = st.sidebar.selectbox("Login as", ["Customer", "Driver"])

# ---------------------------
# Helper: Google Maps Route
# ---------------------------
def get_google_route(origin, destination, waypoints=None):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "waypoints": waypoints,
        "optimizeWaypoints": "true",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

# ---------------------------
# Notifications (Demo)
# ---------------------------
def send_sms(phone, message):
    # Demo: just print message
    print(f"SMS to {phone}: {message}")

# ---------------------------
# CUSTOMER VIEW
# ---------------------------
if role == "Customer":
    st.header("Track Your Parcel")

    parcel_id_input = st.text_input("Enter Parcel ID")
    track_button = st.button("Track Parcel")

    if "tracking_parcel" not in st.session_state:
        st.session_state.tracking_parcel = None

    if track_button and parcel_id_input:
        if parcel_id_input in df["parcel_id"].values:
            st.session_state.tracking_parcel = parcel_id_input
        else:
            st.error("❌ Parcel not found!")
            st.session_state.tracking_parcel = None

    if st.session_state.tracking_parcel:
        parcel = df[df["parcel_id"] == st.session_state.tracking_parcel].iloc[0]

        # Ensure status is string
        status = str(parcel["status"]).strip().lower()

        if status == "placed":
            st.info(f"📦 Your order has been placed, {parcel['customer_name']}!")

        elif status == "warehouse":
            st.info(f"🏢 Your order has reached the warehouse, {parcel['customer_name']}!")

        elif status in ["out_for_delivery", "in_transit"]:
            # Inject JS for auto-refresh every 30s
            refresh_script = """
            <script>
            setTimeout(function(){
                window.location.reload();
            }, 30000);
            </script>
            """
            st.markdown(refresh_script, unsafe_allow_html=True)

            # Initialize driver state
            if "driver_lat" not in st.session_state or "driver_lon" not in st.session_state:
                st.session_state.driver_lat = float(parcel["lat"]) + random.uniform(-0.05, 0.05)
                st.session_state.driver_lon = float(parcel["lon"]) + random.uniform(-0.05, 0.05)
                st.session_state.last_update = time.time()

            # Update location only every 30s
            if time.time() - st.session_state.last_update > 30:
                st.session_state.driver_lat += random.uniform(-0.01, 0.01)
                st.session_state.driver_lon += random.uniform(-0.01, 0.01)
                st.session_state.last_update = time.time()

            driver_lat = st.session_state.driver_lat
            driver_lon = st.session_state.driver_lon
            eta_minutes = random.randint(10, 15)

            st.warning(f"🚚 {parcel['customer_name']}, your parcel {parcel['parcel_id']} is on the way!")
            st.info(f"Driver location: ({driver_lat:.4f}, {driver_lon:.4f}) | ETA: {eta_minutes} minutes")

            # -------------------------------
            # Fetch Google Maps route
            # -------------------------------
            origin = f"{driver_lat},{driver_lon}"
            destination = f"{parcel['lat']},{parcel['lon']}"
            route_data = get_google_route(origin, destination)

            m = folium.Map(location=[parcel["lat"], parcel["lon"]], zoom_start=12)

            if route_data.get("status") == "OK":
                coords = polyline.decode(route_data["routes"][0]["overview_polyline"]["points"])
                folium.PolyLine(coords, color="blue", weight=5, opacity=0.7).add_to(m)

            # Driver marker
            folium.Marker(
                [driver_lat, driver_lon],
                popup="Driver",
                icon=folium.Icon(color="green")
            ).add_to(m)

            # Customer/destination marker
            folium.Marker(
                [parcel["lat"], parcel["lon"]],
                popup=f"{parcel['customer_name']}'s Location",
                icon=folium.Icon(color="red")
            ).add_to(m)

            st_folium(m, width=700, height=500)

        elif status == "delivered":
            st.success(f"✅ {parcel['customer_name']}, your parcel {parcel['parcel_id']} has been delivered!")
            st.subheader("📝 Give Feedback")
            feedback = st.text_area("Write your feedback")
            rating = st.slider("Rate your delivery experience", 1, 5, 5)
            if st.button("Submit Feedback"):
                st.success("Thanks for your feedback!")

# ---------------------------
# DRIVER VIEW
# ---------------------------
elif role == "Driver":
    st.header("Driver Dashboard")
    driver_id = st.selectbox("Select Your Driver ID", df["driver_id"].unique())
    driver_parcels = df[df["driver_id"] == driver_id]

    st.subheader("Your Assigned Parcels")
    st.dataframe(driver_parcels[["parcel_id","customer_name","address","status"]])

    st.subheader("Start Delivery (QR Scan Simulation)")
    parcel_to_deliver = st.selectbox("Select Parcel", driver_parcels["parcel_id"])

    if "active_parcel" not in st.session_state:
        st.session_state.active_parcel = None

    if st.button("Start Delivery"):
        st.session_state.active_parcel = parcel_to_deliver
        df.loc[df["parcel_id"] == parcel_to_deliver, "status"] = "out_for_delivery"
        df.loc[df["parcel_id"] == parcel_to_deliver, "start_time"] = datetime.now()
        save_data(df)

        parcel = df[df["parcel_id"] == parcel_to_deliver].iloc[0]
        send_sms(parcel["phone"], f"Hello {parcel['customer_name']}, your parcel {parcel_to_deliver} is out for delivery! ETA approx 10-15 mins")

        st.success(f"Started delivery for {parcel_to_deliver}. Notification sent!")

    # Show route map for active parcel
    if st.session_state.active_parcel:
        parcel = df[df["parcel_id"] == st.session_state.active_parcel].iloc[0]
        origin = "19.0760,72.8777"  # warehouse
        destination = f"{parcel['lat']},{parcel['lon']}"
        route_data = get_google_route(origin, destination)
        if route_data.get("status") == "OK":
            coords = polyline.decode(route_data["routes"][0]["overview_polyline"]["points"])
            m = folium.Map(location=[parcel["lat"], parcel["lon"]], zoom_start=12)
            folium.PolyLine(coords, color="blue", weight=4, opacity=0.7).add_to(m)
            folium.Marker([parcel["lat"], parcel["lon"]], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
            st_folium(m, width=700, height=500)
        else:
            # fallback map if route fails
            m = folium.Map(location=[parcel["lat"], parcel["lon"]], zoom_start=12)
            folium.Marker([parcel["lat"], parcel["lon"]], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
            st_folium(m, width=700, height=500)

    if st.button("Mark as Delivered"):
        if st.session_state.active_parcel:
            df.loc[df["parcel_id"] == st.session_state.active_parcel, "status"] = "delivered"
            save_data(df)
            parcel = df[df["parcel_id"] == st.session_state.active_parcel].iloc[0]
            send_sms(parcel["phone"], f"✅ {parcel['customer_name']}, your parcel {parcel['parcel_id']} has been delivered!")
            st.success(f"{st.session_state.active_parcel} marked as delivered. Waiting for customer confirmation...")
            st.session_state.active_parcel = None
