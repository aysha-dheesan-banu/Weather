# 🌦️ WeatherWise 360°

A dynamic and user-friendly Streamlit weather dashboard that displays real-time weather data, visual trends, and mood-based Spotify music recommendations — all in one place.

---

## 🔍 Overview

**WeatherWise 360°** is a powerful, intuitive weather app built with Python and Streamlit that:

- Fetches real-time weather from **OpenWeatherMap API**
- Visualizes temperature trends using **Plotly**
- Displays interactive maps with **Folium**
- Suggests mood-based playlists using **Spotify API**
- Stores history in **SQLite**
- Offers smart weather-based themes and alerts

---

## 🎯 Features

- 🌍 **Search Any City** – Get real-time weather conditions worldwide  
- 🎨 **Weather-Themed UI** – Dynamic backgrounds based on current weather  
- ⚠️ **Weather Alerts** – Warnings for storms, heatwaves, and more  
- 📊 **Visualization** – Plot city comparisons and temperature trends  
- 🎵 **Spotify Playlists** – Music recommendations tailored to weather mood  
- 📜 **Weather History** – Stored in a local SQLite database  
- 🗺️ **City Map** – Interactive map showing the city’s location  
- 🔮 **Forecast & Prediction** – AI-powered next-day temperature prediction  
- 🧭 **Location Auto-Detect** – Optional geolocation using IP  

---

## 🧰 Tech Stack

| Category        | Technologies Used                                |
|----------------|---------------------------------------------------|
| Frontend       | Streamlit                                         |
| Backend        | Python, OpenWeatherMap API                        |
| Data Storage   | SQLite                                            |
| Mapping        | Folium                                            |
| Visualization  | Plotly                                            |
| Music API      | Spotify (via Spotipy)                             |
| Geolocation    | Geocoder                                          |

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/weatherwise360.git
cd weatherwise360
#To Run:
pip install -r requirements.txt
streamlit run weather_app.py
