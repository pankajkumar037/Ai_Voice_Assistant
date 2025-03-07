import requests


def fetch_weather(location):
    """
    Fetch the weather details for a given location using Open-Meteo.
    """
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"

    try:
        # Fetch latitude and longitude
        geocode_response = requests.get(geocode_url)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()

        if "results" not in geocode_data or len(geocode_data["results"]) == 0:
            return f"Sorry, I couldn't find weather details for '{location}'. Please try another location."

        latitude = geocode_data["results"][0]["latitude"]
        longitude = geocode_data["results"][0]["longitude"]
        location_name = geocode_data["results"][0]["name"]

        # Fetch weather details
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if "current_weather" in weather_data:
            current_weather = weather_data["current_weather"]
            temperature = current_weather["temperature"]
            windspeed = current_weather["windspeed"]
            weather_code = current_weather.get("weathercode", -1)

            weather_conditions = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Foggy",
                48: "Depositing rime fog",
                51: "Light drizzle",
                53: "Moderate drizzle",
                55: "Dense drizzle",
                61: "Slight rain",
                63: "Moderate rain",
                65: "Heavy rain",
                71: "Slight snow",
                73: "Moderate snow",
                75: "Heavy snow",
                80: "Rain showers",
                81: "Moderate rain showers",
                82: "Heavy rain showers",
                95: "Thunderstorm",
                96: "Thunderstorm with hail",
            }
            weather_description = weather_conditions.get(weather_code, "Unknown conditions")

            temperature_description = (
                "hot" if temperature > 30 else "cold" if temperature < 15 else "moderate"
            )

            return (f"The current weather in {location_name} is {weather_description} with a temperature of "
                    f"{temperature}°C ({temperature_description}) and a windspeed of {windspeed} km/h.")
        else:
            return "Sorry, I couldn't fetch the weather details at this time."

    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching weather data: {e}"

def handle_weather(user_input):
    """
    Handles weather-related queries interactively with the user.
    """
    global current_functionality, conversation_context

    # Directly fetch weather if functionality is already set to 'weather'
    if current_functionality == "weather":
        if user_input.lower() == "exit":
            current_functionality = None
            return "Exited the weather functionality. How can I assist you next?"
        return fetch_weather(user_input.strip())

    # Detect if location is already mentioned in the first input
    if user_input.lower() in ["weather", "weather update", "what's the weather outside"]:
        current_functionality = "weather"
        return "For which location would you like to get the weather?"

    # Assume the user input is a location on the first call
    current_functionality = "weather"
    return fetch_weather(user_input.strip())