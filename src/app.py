#!/usr/bin/env python3
"""
Weather Tool for offs.run
Fetches current weather data for a given location using wttr.in service
"""

from flask import Flask, request, jsonify
import json
import urllib.request
import urllib.error
import os

app = Flask(__name__)

def get_weather(location):
    """Fetch weather data from wttr.in"""
    # Format location for URL (replace spaces with +)
    formatted_location = location.replace(' ', '+')
    url = f"https://wttr.in/{formatted_location}?format=j1"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'offs.run-weather-tool')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        # Extract current condition
        current = data['current_condition'][0]
        weather_desc = current['weatherDesc'][0]['value']
        temp_c = current['temp_C']
        temp_f = current['temp_F']
        humidity = current['humidity']
        windspeed_kmh = current['windspeedKmph']
        observation_time = current.get('observation_time', '')
        
        result = {
            "location": location,
            "weather": weather_desc,
            "temperature_c": temp_c,
            "temperature_f": temp_f,
            "humidity_percent": humidity,
            "windspeed_kmh": windspeed_kmh,
            "observation_time": observation_time
        }
        
        return {
            "success": True,
            "result": result
        }
        
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"Failed to fetch weather data: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "weather-tool"})

@app.route('/execute', methods=['POST'])
def execute():
    """Execute the weather tool"""
    try:
        # Get JSON data from request
        if not request.is_json:
            return jsonify({"success": False, "error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        params = data.get('params', {})
        
        # Extract location parameter
        location = params.get('location')
        if not location:
            return jsonify({"success": False, "error": "Missing required parameter: location"}), 400
        
        # Get weather data
        result = get_weather(location)
        
        # Return result in offs.run expected format
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Tool execution failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)