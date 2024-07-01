from app import Flask, request, jsonify,requests

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    client_ip = request.remote_addr
    
    
    geo_response = requests.get(f'http://ip-api.com/json/{client_ip}')
    geo_data = geo_response.json()
    city = geo_data.get('city', 'Unknown')

    
    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=a06aa16d020f90c6b38f45a9916f8643&units=metric')
    weather_data = weather_response.json()
    temperature = weather_data['main']['temp']

    return jsonify({
        'client_ip': client_ip,
        'location': city,
        'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
    })

if __name__ == '__main__':
    app.run(debug=True)
