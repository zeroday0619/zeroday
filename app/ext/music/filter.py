import functools
import pymongo
import asyncio
import aiohttp

from app.controller import config
from app.controller.logger import Logger
from app.ext.performance import run_in_threadpool


class SafetySearch:
    """BASE Project: https://github.com/zeroday0619/SafetySearch"""

    def __init__(self):
        self.logger = Logger.generate_log()

        self.url = "https://openapi.naver.com/v1/search/adult.json"
        self.safty_msg = "해당 검색어는 Safety Search 에 의해 사용하실수 없습니다."

        # Mongo DB Credential
        self.MongoDB_URL = config["mongodb_url"]
        self.MongoDB_PORT = config["mongodb_port"]

        # NAVER API Authentication
        self.headers = {
            "X-Naver-Client-Id": config["X-Naver-Client-Id"],
            "X-Naver-Client-Secret": config["X-Naver-Client-Secret"],
        }

    @Logger.set()
    async def requests(self, data):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url=self.url, params=data) as resp:
                result = await resp.json()
        return result

    @Logger.set()
    async def adult_filter(self, search: str, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        data = {"query": search}

        params_clent = functools.partial(pymongo.MongoClient, self.MongoDB_URL, self.MongoDB_PORT)
        client = await loop.run_in_executor(None, params_clent)

        db = client["adult_filter"]
        collection = db["database"]

        collection.create_index(
            [
                ("filter_string", pymongo.ASCENDING),
                ("green", pymongo.ASCENDING)
            ]
        )
        default_filter = [
            {"filter_string": "[붕탁]빌리와 구슬고자"},
            {"filter_string": "**A Simple Favor (2018) - Sleeping With My Brother Scene (2/10) | Movieclips**"},
            {"filter_string": "sex"}
        ]
        await run_in_threadpool(
            lambda: collection.insert_many(default_filter)
        )
        mo = await run_in_threadpool(
            lambda: db.database.find_one({"filter_string": search})
        )
        try:
            if mo != None:
                check = mo["filter_string"]
                if check == search:
                    self.logger.info(f"DATABASE FILTER: {self.safty_msg}")
                    return 1
                else:
                    self.logger.error("DATABASE FILTER: System Error")
                    return 1
            else:
                mx = await run_in_threadpool(
                    lambda: db.database.find_one({"green": search})
                )
                if mx == None:
                    resp = await self.requests(data)
                    if resp["adult"] == "1":
                        self.logger.info(f"NAVER SEARCH API: {self.safty_msg}")
                        query = [{"filter_string": search}]
                        await run_in_threadpool(lambda: collection.insert_many(query))
                        return 1
                    elif resp["adult"] == "0":
                        self.logger.info("NAVER SEARCH API: 정상")
                        query2 = [{"green": search}]
                        await run_in_threadpool(lambda: collection.insert_many(query2))
                        return search
                    else:
                        self.logger.error("NAVER SEARCH API: Error")
                        return 1
                else:
                    self.logger.info("DATABASE FILTER: 정상")
                    return search
        except Exception as ex:
            self.logger.error(ex)
            pass


safe = SafetySearch()
