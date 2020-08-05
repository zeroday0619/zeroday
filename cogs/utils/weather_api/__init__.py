from Utils import config
from .request import Request


class WeatherAPI:
    def __init__(self):
        self.service_key: str = config['weather_api_key']
        self.source = Request(
            service_key=self.service_key
        )
    
    async def load_weather_data(self):
        source = await self.source.requests()
        return source