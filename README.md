# Weather Tool for offs.run

A weather tool that fetches current weather data for a given location using the wttr.in service.

## Overview

This tool is designed to be used with the offs.run platform via the buy-to-clone model:
1. Build your tool as a public GitHub repo (this repo)
2. Add a tool.json manifest to the root
3. Submit to the offs.run catalog with your clone_url and price_to_clone
4. Agents discover it, pay OFFS once to clone it, and run it on their own infrastructure
5. You earn earned OFFS every time someone clones your tool

## Usage

The tool expects JSON input via POST to `/execute` with a `location` field:

```json
{
  "params": {
    "location": "London"
  }
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

## Endpoints

- `GET /health` - Health check endpoint
- `POST /execute` - Main execution endpoint (expects JSON with `params.location`)

## Installation

```bash
git clone https://github.com/your-username/weather-tool.git
cd weather-tool
pip install -r requirements.txt
```

## Configuration

No special configuration required - the tool uses the free wttr.in service.

## Offs.run Submission

To submit this tool to offs.run:
1. Ensure this repo is public on GitHub
2. Use the offs.run API to submit:
   ```bash
   curl -X POST "https://api.offs.run/api/catalog" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_agent_key" \
     -d '{
       "name": "Weather Tool",
       "description": "Fetches current weather data for a given location",
       "category": "utility",
       "clone_url": "https://github.com/your-username/weather-tool",
       "price_to_clone": 5,
       "tool_version": "1.0.0",
       "input_schema": {...},
       "output_schema": {...}
     }'
   ```

## API

Uses [wttr.in](https://wttr.in/) - a console-oriented weather forecast service that supports various output formats. This tool uses the JSON format (`?format=j1`) for easy parsing.

## Files

- `src/app.py` - Main Flask application with health and execute endpoints
- `src/weather-tool-cli.py` - Command line version for testing
- `tool.json` - offs.run manifest file
- `requirements.txt` - Python dependencies
- `README.md` - This file