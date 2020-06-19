from Utils import config
from .performance import run_in_threadpool
import pymongo
import aiohttp

class SafetySearch:
    """
	BASE Project: https://github.com/zeroday0619/SafetySearch
	"""

    def __init__(self):
        self.url = "https://openapi.naver.com/v1/search/adult.json"
        self.safty_msg = "해당 검색어는 Safety Search 에 의해 사용하실수 없습니다."

        # Mongo DB Credential
        self.MongoDB_URL = config['mongodb_url']
        self.MongoDB_PORT = config['mongodb_port']

        # NAVER API Authentication
        self.headers = {
            "X-Naver-Client-Id": config['X-Naver-Client-Id'],
            "X-Naver-Client-Secret": config['X-Naver-Client-Secret']
        }

    async def requests(self, data):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url=self.url, params=data) as resp:
                result = await resp.json()
        return result

    async def adult_filter(self, search: str):
        data = {
            "query": search
        }
        client = await run_in_threadpool(lambda: pymongo.MongoClient(self.MongoDB_URL, self.MongoDB_PORT))
        db = client['adult_filter']
        collection = db['database']

        mo = await run_in_threadpool(lambda: db.database.find_one({"filter_string": search}))
        try:
            if mo != None:
                check = mo['filter_string']
                if check == search:
                    print("DB 조회\n" + self.safty_msg)
                    return 1
                else:
                    print("DB 조회\n" + "System Error")
                    return 2
            else:
                mx = await run_in_threadpool(lambda: db.database.find_one({"green": search}))
                if mx == None:
                    resp = await self.requests(data)
                    if resp['adult'] == '1':
                        print("API 사용\n" + self.safty_msg)
                        query = [
                            {
                                "filter_string": search
                            }
                        ]
                        await run_in_threadpool(lambda: collection.insert_many(query))
                        return 1
                    elif resp['adult'] == '0':
                        print("API 사용\n정상")
                        query2 = [
                            {
                                "green": search
                            }
                        ]
                        await run_in_threadpool(lambda: collection.insert_many(query2))
                        return search
                    else:
                        print("API 사용\nSystem Error")
                        return 2
                else:
                    print("DB 조회 \n 정상")
                    return search
        except Exception as ex:
            print(ex)
            pass


safe = SafetySearch()
