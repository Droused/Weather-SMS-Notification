import schedule
import time
import requests
from twilio.rest import Client

def get_weather(latitude, longitude):
    api= "api"
    base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api}"
    response = requests.get(base_url)
    data = response.json()
    return data

def kel_to_fah(kelvin):
    return ((kelvin - 273.15)  * 9/5) + 32

def send_text_message(body):
    account_sid = 'twilio_sid'
    auth_token = 'twilio_token'
    from_phone_number = 'twilio_number'
    to_phone_number = 'your_number'

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=from_phone_number,
        to=to_phone_number,
    )
    print("Text message sent!")

def send_weather_update():
    latitude = 40.71427
    longitude = -74.00597

    weather_data = get_weather(latitude, longitude)
    temperature_kelvin = weather_data["main"]["temp"]
    relative_humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    location = weather_data["name"]
    tempFahrenheit = kel_to_fah(temperature_kelvin)
    print(tempFahrenheit)

    weather_info = (
        f"Good Morning!\n"
        f"Current Weather in {location}:\n"
        f"Temperature: {tempFahrenheit:.2f}ºF\n"
        f"Relative Humidity: {relative_humidity}%\n"
        f"Wind Speed: {wind_speed} m/s"
    )

    print(weather_info)


def main():
    schedule.every().day.at("08:00").do(send_weather_update)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
