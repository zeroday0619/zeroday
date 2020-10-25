from aiohttp import ClientSession


class Aniplus:
    def __init__(self):
        self.apiUrl = 'https://api.aniplustv.com:3100/'
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://www.aniplustv.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'api.aniplustv.com:3100',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
            'Accept-Language': 'en-us',
            'Referer': 'https://www.aniplustv.com/',
            'Connection': 'keep-alive'
        }
    
    async def requests(self, api_dir: str):
        async with ClientSession(headers=self.headers) as session:
            async with session.get(url=self.apiUrl + api_dir, allow_redirects=False) as response:
                status = response.status
                if 200 != status:
                    del session, response, status
                    return None
                elif 200 == status:
                    json_data = await response.json()
                    return json_data
    
    async def updateContent(self):
        api_dir = "updateContent?userid="
        data = await self.requests(api_dir=api_dir)
        if data is None:
            del api_dir
            print("Warnning: response data is empty!")
            return None
        return data