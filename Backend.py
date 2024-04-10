# app.py

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
GOOGLE_GEOCODING_API_KEY = 'AIzaSyCK6OVZa9TroQRa8jJ8ozFpr8HP3vjvrlQ'

@app.route('/solar-potential', methods=['POST'])
def get_solar_potential():
    try:
        address = request.json.get('address')
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        
        # Convert address to latitude and longitude
        geocoding_response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_GEOCODING_API_KEY}')
        geocoding_response.raise_for_status()
        geocoding_data = geocoding_response.json()

        if geocoding_data['status'] != 'OK' or len(geocoding_data['results']) == 0:
            return jsonify({'error': 'Failed to geocode address'}), 400

        location = geocoding_data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        
        # Use latitude and longitude to get solar potential data
        response = requests.get(f'https://solar.googleapis.com/v1/buildingInsights:findClosest?key={GOOGLE_GEOCODING_API_KEY}&lat={latitude}&lng={longitude}')
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes

        solar_potential_data = response.json()
        return jsonify(solar_potential_data)
    except requests.exceptions.RequestException as e:
        print('Error fetching solar potential data:', e)
        return jsonify({'error': 'Failed to fetch solar potential data'}), 500
    except Exception as e:
        print('Error:', e)
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)



