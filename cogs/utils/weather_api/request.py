import aiohttp


# 'http://apis.data.go.kr/1360000/WthrWrnInfoService/getPwnStatus
# ServiceKey=서비스키
# ServiceKey=-
# pageNo=1
# numOfRows=10
# dataType=json'

class Request:
    def __init__(self, service_key):
        self.service_key = service_key
        self.url = f"http://apis.data.go.kr/1360000/WthrWrnInfoService/getPwnStatus?ServiceKey={self.service_key}&pageNo=1&numOfRows=10&dataType=json"
    
    async def requests(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                res = await resp.json()
            return res
