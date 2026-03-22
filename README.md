# Weather Tool for offs.run

A simple weather tool that fetches current weather data for a given location using the wttr.in service.

## Usage

The tool expects JSON input via stdin with a `location` field:

```json
{
  "location": "London"
}
```

It returns JSON output with weather information:

```json
{
  "success": true,
  "result": {
    "location": "London",
    "weather": "Partly cloudy",
    "temperature_c": 15,
    "temperature_f": 59,
    "humidity_percent": 72,
    "windspeed_kmh": 10,
    "observation_time": "02:00 PM"
  }
}
```

## Examples

```bash
# Get weather for New York
echo '{"location": "New York"}' | python3 weather-tool.py

# Get weather for Tokyo
echo '{"location": "Tokyo"}' | python3 weather-tool.py
```

## Installation

No special installation required - just needs Python 3.x and internet access to reach wttr.in.

## Offs.run Integration

This tool is designed to be used with the offs.run platform. To use it on offs.run:
1. Build/publish the tool to the offs.run catalog
2. Others can clone and execute it for 1 OFFS per execution
3. The tool creator earns OFFS when others clone their tool

## API

Uses [wttr.in](https://wttr.in/) - a console-oriented weather forecast service that supports various output formats. This tool uses the JSON format (`?format=j1`) for easy parsing.