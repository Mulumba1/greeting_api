from app import Flask, request, jsonify,requests

app = Flask(__name__)

WEATHER_API_KEY = '9af52fb456634278ab780110240207'

def get_weather_by_ip(ip, api_key):
    weather_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={ip}&aqi=no'
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        weather_data = response.json()
        city = weather_data['location']['name']
        temperature = weather_data['current']['temp_c']
        return city, temperature
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None, None

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    
    
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    
    
    city, temperature = get_weather_by_ip(client_ip, WEATHER_API_KEY)
    temperature_str = f"{temperature} degrees Celsius" if temperature is not None else "unavailable"
    
    return jsonify({
        'client_ip': client_ip,
        'location': city if city else 'Unknown',
        'greeting': f'Hello, {visitor_name}!, the temperature is {temperature_str} in {city if city else "Unknown"}'
    })

if __name__ == '__main__':
    app.run(debug=True)
