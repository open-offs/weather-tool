#!/usr/bin/env python3
"""
Weather tool for offs.run platform
Fetches current weather data for a given location
"""

import json
import sys
import urllib.request
import urllib.error

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
        
        result = {
            "location": location,
            "weather": weather_desc,
            "temperature_c": temp_c,
            "temperature_f": temp_f,
            "humidity_percent": humidity,
            "windspeed_kmh": windspeed_kmh,
            "observation_time": current.get('observation_time', '')
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

def main():
    """Main entry point for offs.run tool execution"""
    try:
        # Read input from stdin (offs.run sends JSON params)
        input_data = sys.stdin.read().strip()
        if not input_data:
            # For testing - default location
            params = {"location": "New York"}
        else:
            params = json.loads(input_data)
        
        location = params.get("location", "New York")
        
        # Get weather data
        result = get_weather(location)
        
        # Output JSON result (offs.run expects this format)
        print(json.dumps(result))
        
    except json.JSONDecodeError:
        print(json.dumps({
            "success": False,
            "error": "Invalid JSON input"
        }))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": f"Tool execution failed: {str(e)}"
        }))

if __name__ == "__main__":
    main()