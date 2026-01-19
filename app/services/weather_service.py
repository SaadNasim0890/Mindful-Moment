import httpx
from typing import Dict

class WeatherService:
    async def get_current_context(self, lat: float = None, lon: float = None) -> str:
        # Default to NYC if no location provided
        latitude = lat if lat is not None else 40.71
        longitude = lon if lon is not None else -74.01
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,weather_code"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                data = response.json()
                
                current = data.get('current', {})
                is_day = "Daytime" if current.get('is_day') == 1 else "Nighttime"
                temp = current.get('temperature_2m')
                code = current.get('weather_code', 0)
                
                # Simple WMO code mapping
                condition = "Clear"
                if 1 <= code <= 3: condition = "Cloudy"
                elif 45 <= code <= 48: condition = "Foggy"
                elif 51 <= code <= 67: condition = "Rainy"
                elif 71 <= code <= 77: condition = "Snowy"
                elif 80 <= code <= 82: condition = "Heavy Rain"
                elif 95 <= code <= 99: condition = "Thunderstorm"
                
                return f"Condition: {condition}, Time: {is_day}, Temperature: {temp}C"
        except Exception as e:
            print(f"Weather API Error: {e}")
            return "Time: Daytime (API Unavailable)"
