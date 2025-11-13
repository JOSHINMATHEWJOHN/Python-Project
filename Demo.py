import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

API_KEY = "7b6722719d3793823c96a48353049911"
#streamlit run C:\Users\hp\PycharmProjects\PythonProject\Python Project\Demo.py

def convert_to_celsius(temperature_in_kelvin):
    return temperature_in_kelvin - 273.15

def format_timezone_offset(offset_seconds):
    hours = offset_seconds // 3600
    minutes = abs((offset_seconds % 3600) // 60)
    return f"GMT{'+' if hours >= 0 else '-'}{abs(hours):02}:{minutes:02}"

def find_current_weather(city):
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    weather_data = requests.get(base_url).json()
    st.json(weather_data)
    try:
        general = weather_data['weather'][0]['main']
        t=weather_data['weather'][0]['description']
        icon_id = weather_data['weather'][0]['icon']
        temperature = round(convert_to_celsius(weather_data['main']['temp']))
        icon = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
        # Extract time and timezone
        timestamp = weather_data['dt']
        timezone_offset = weather_data['timezone']  # in seconds
        utc_time = datetime.utcfromtimestamp(timestamp)
        local_time = utc_time + timedelta(seconds=timezone_offset)
        # Format time and timezone
        timezone_str = format_timezone_offset(timezone_offset)
        formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S") + f" {timezone_str}"

    except KeyError:
        st.error("City Not Found")
        st.stop()

    return general,temperature,icon,t,formatted_time

def main():
    st.header("🌦️ Weather ")
    city = st.text_input("Enter the City").lower()
    if st.button("Find"):
        general, temperature, icon, t,formatted_time= find_current_weather(city)
        st.write(f"Local Date & Time in **{city.title()}**: **{formatted_time}**")
        col_1, col_2 = st.columns(2)
        with col_1:
            st.metric(label="Temperature", value=f"{temperature}°C")
        with col_2:
            st.write(general,"-",t)
            st.image(icon)

if __name__ == '__main__':
    main()


