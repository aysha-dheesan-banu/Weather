import streamlit as st
import requests
import pandas as pd
import sqlite3
import folium
from streamlit_folium import folium_static
import plotly.express as px
from datetime import datetime, timedelta
import geocoder
import random

# Set page config
st.set_page_config("🌦️ WeatherWise 360°", layout="centered")

# Sidebar
st.sidebar.image("D:/images/weather.png", caption="🌤️ WeatherWise 360°", use_container_width=True)
st.sidebar.title("Weather Dashboard")
st.sidebar.markdown("Stay ahead of the weather!")

# Rotating weather tip
tips = [
    "Carry an umbrella even if it just looks cloudy!",
    "Hydrate well in hot weather!",
    "Layer up to stay warm in the cold!",
    "Check wind speed before cycling!"
]
random_tip = random.choice(tips)
st.sidebar.markdown("---")
st.sidebar.markdown(f"🌈 **Weather Tip:** {random_tip}")

# Unit toggle
unit = st.sidebar.radio("Select Temperature Unit", ["Celsius", "Fahrenheit"])
unit_param = "metric" if unit == "Celsius" else "imperial"

# Notification Scheduler (Mocked)
st.sidebar.markdown("---")
if st.sidebar.checkbox("🔔 Morning Weather Reminder"):
    st.sidebar.success("You'll get a reminder to check weather every morning!")

# Main title
st.title("🌦️ WeatherWise 360°")
st.markdown("""
Stay ahead of the weather! 🌍☀️🌧️☁️❄️  
Enter a city to get live conditions, trends, maps, alerts, playlists & predictions.
""")

# Database setup
with sqlite3.connect("weather_log.db") as conn:
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather(
            city TEXT, temperature REAL, humidity INTEGER,
            wind_speed REAL, description TEXT,
            lat REAL, lon REAL, date_time TEXT
        )
    ''')
    conn.commit()

    # API setup
    API_KEY = "6961d0f0d00d6c1abe35bc5f3cba6afa"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    # User input
    user_location = geocoder.ip('me')
    suggested_city = user_location.city if user_location else ""
    city = st.text_input("🏙️ Enter City Name", suggested_city or "Chennai")

    if st.button("🔍 Get Weather"):
        if city:
            params = {"q": city, "appid": API_KEY, "units": unit_param}
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                description = data['weather'][0]['description'].title()
                icon_code = data['weather'][0]['icon']
                lat = data['coord']['lat']
                lon = data['coord']['lon']
                date_time = datetime.now().strftime("%b %d, %Y %I:%M %p")

                # Geo-Fencing
                user_city = suggested_city
                if user_city and user_city.lower() != city.lower():
                    st.warning("⚠️ You're not currently in this city. Plan your travel accordingly!")

                # Dynamic background theme (Emoji only)
                theme_map = {
                    "clear": "☀️ Bright Sky Theme",
                    "rain": "🌧️ Rainy Background",
                    "snow": "❄️ Snowflakes Theme",
                    "cloud": "☁️ Cloudy Theme"
                }
                matched_theme = next((v for k, v in theme_map.items() if k in description.lower()), "🌥️ Default Sky Theme")
                st.info(f"🎨 Theme Applied: {matched_theme}")

                # Weather Display
                emoji_map = {
                    "clear": "☀️",
                    "rain": "🌧️",
                    "cloud": "☁️",
                    "snow": "❄️"
                }
                emoji = next((v for k, v in emoji_map.items() if k in description.lower()), "❓")
                st.subheader(f"{emoji} Weather in {city}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("🌡️ Temperature", f"{temperature}°{unit[0]}")
                    st.metric("💧 Humidity", f"{humidity}%")
                    st.metric("🌬️ Wind Speed", f"{wind_speed} m/s")
                with col2:
                    st.markdown(f"![icon](http://openweathermap.org/img/wn/{icon_code}@2x.png)")
                    st.markdown(f"**📍 Location**: {city}")
                    st.markdown(f"**📝 Description**: {description}")
                    st.markdown(f"**🕓 Time**: {date_time}")

                # Mood-based Music Recommendation
                if "rain" in description.lower():
                    music = "https://open.spotify.com/playlist/37i9dQZF1DX0SM0LYsmbMT"
                elif "clear" in description.lower():
                    music = "https://open.spotify.com/playlist/37i9dQZF1DX1BzILRveYHb"
                else:
                    music = "https://open.spotify.com/playlist/37i9dQZF1DWXe9gFZP0gtP"
                st.markdown(f"🎶 **Mood Playlist:** [Listen on Spotify]({music})")

                # Map display
                m = folium.Map(location=[lat, lon], zoom_start=10)
                folium.Marker([lat, lon], tooltip=f"{city}: {description}").add_to(m)
                folium_static(m)

                # Store in database
                c.execute('''INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                          (city, temperature, humidity, wind_speed, description, lat, lon, date_time))
                conn.commit()

                # Predict tomorrow's temperature (mocked)
                predicted_temp = round(temperature + random.uniform(-2.5, 2.5), 2)
                st.markdown(f"🧠 **AI Prediction:** Tomorrow’s temperature in {city} may be around {predicted_temp}°{unit[0]} (±2°C)")

                # Event Countdown
                pongal_date = datetime(datetime.now().year, 1, 15)
                days_left = (pongal_date - datetime.now()).days
                if days_left > 0:
                    st.markdown(f"📅 **Event Countdown:** Pongal is in {days_left} days! 🌤️ Expected weather: Sunny and dry")

                # Severe Weather Alerts
                alerts = ["storm", "thunder", "extreme", "heat", "wind"]
                if any(alert in description.lower() for alert in alerts):
                    st.error(f"🚨 Weather Alert: {description} in {city}. Stay indoors and take precautions!")
            else:
                st.error("❌ Failed to retrieve weather data. Check the city name or API key.")

    # History & Plot
    st.subheader("📈 Weather Search History")
    c.execute("SELECT * FROM weather")
    rows = c.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=['City', 'Temperature', 'Humidity', 'Wind Speed',
                                         'Description', 'Latitude', 'Longitude', 'Date/Time'])
        st.dataframe(df.tail(10))

        # Plot
        fig = px.line(df.tail(10), x='Date/Time', y='Temperature', color='City', title="Temperature Trends")
        st.plotly_chart(fig)

        # Comparative Analysis
        st.subheader("📊 Comparative Climate Analysis")
        cities = df['City'].unique().tolist()
        if len(cities) > 1:
            city1 = st.selectbox("Select First City", cities, index=0)
            city2 = st.selectbox("Select Second City", cities, index=1)
            df_compare = df[df['City'].isin([city1, city2])]
            fig2 = px.line(df_compare, x='Date/Time', y='Temperature', color='City',
                           title=f"{city1} vs {city2} - Temperature Comparison")
            st.plotly_chart(fig2)

        if st.button("🗑️ Clear History"):
            c.execute("DELETE FROM weather")
            conn.commit()
            st.success("Cleared weather history!")

# Footer
st.markdown("---")
st.markdown("© 2025 WeatherWise 360° | Built with ❤️ using Streamlit")


