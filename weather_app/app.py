from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    prediction = None

    if request.method == 'POST':
        city = request.form['city']
        api_key = "2433a38bb716009ba0ef841a5198c766"  # Replace with your OpenWeather API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            # Extract relevant information
            city_name = data['name']
            country = data['sys']['country']
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            # Prepare weather info and prediction
            weather_info = {
                'city': city_name,
                'country': country,
                'temperature': temperature,
                'description': weather_description,
                'humidity': humidity,
                'wind_speed': wind_speed
            }

            # Predict whether it will rain
            if "rain" in weather_description.lower() or "drizzle" in weather_description.lower():
                prediction = "It is likely to rain."
            else:
                prediction = "It is unlikely to rain."
        
        except requests.exceptions.HTTPError as err:
            weather_info = {"error": "City not found or API error."}

    return render_template('index.html', weather_info=weather_info, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
