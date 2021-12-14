import aiohttp
import kss
import discord
from app.module import RegexFilter
from app.controller.logger import Logger
from app.controller import kakao_rest_api_key
from extensions.tts._extension_error import (
    BAD_REQUEST_EXCEPTION,
    UNAUTHORIZED_EXCEPTION,
    FORBIDDEN_EXCEPTION,
    TOO_MANY_REQUEST_EXCEPTION,
    INTERNAL_SERVER_ERROR_EXCEPTION,
    BAD_GATEWAY_EXCEPTION,
    SERVICE_UNAVAILABLE_EXCEPTION
)


class KakaoOpenAPI:
    def __init__(self) -> None:
        self.safe = RegexFilter()
        self.logger = Logger.generate_log()
        self.rest_api_url = "https://kakaoi-newtone-openapi.kakao.com"
        self.rest_api_key = kakao_rest_api_key

    @staticmethod
    @Logger.set()
    def status_code(status_code: int):
        """

        :param status_code: HTTP 상태 코드
        """
        if status_code == 200:
            pass
        elif status_code == 400:
            raise BAD_REQUEST_EXCEPTION()
        elif status_code == 401:
            raise UNAUTHORIZED_EXCEPTION()
        elif status_code == 403:
            raise FORBIDDEN_EXCEPTION()
        elif status_code == 429:
            raise TOO_MANY_REQUEST_EXCEPTION()
        elif status_code == 500:
            raise INTERNAL_SERVER_ERROR_EXCEPTION()
        elif status_code == 502:
            raise BAD_GATEWAY_EXCEPTION()
        elif status_code == 503:
            raise SERVICE_UNAVAILABLE_EXCEPTION()
        else:
            raise Exception("알수없는 오류가 발생하였습니다.")

    def EmbedSaftySearch(self, data):
        embed = discord.Embed(
            title="불법·유해 미디어에 대한 차단 안내",
            url="http://warning.or.kr/",
            description=f"```ini\n검열 시스템 3.0~```",
            color=discord.Color.blurple(),
        ).set_image(
            url="https://cdn.zeroday0619.dev/img/a943b980d720c07de45b2ac88edaa116.jpg"
        ).add_field(
            name="Blocked words", value=str(data.strip()), inline=False
        ).set_footer(
            text="Safe Search | Version: alpha 1.0.0",
            icon_url="https://cdn.zeroday0619.dev/img/cc5bb239a7518bfcd02c9dd2d4e6bfe0.jpg"
        )
        return embed

    @Logger.set()
    def request_header_generator(self) -> dict:
        headers = {
            "Content-Type": "application/xml",
            "Authorization": f"KakaoAK {self.rest_api_key}"
        }
        return headers

    @Logger.set()
    def speak_data_generator(self, source: str) -> str:
        """SSML 변환

        :param source: 음성합성할 문장이나 단어
        :return: ssml
        """
        sc = source.replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("(", "").replace(")", "")
        dat = []
        data = dat.append
        for sent in kss.split_sentences(self.safe.suicide(sc)):
            self.logger.info(sent)
            data('<prosody rate="medium" volume="loud">' + sent + '<break/></prosody>')

        text = f"""
        <speak> 
            <voice name="WOMAN_READ_CALM"> 
                {str(''.join(dat))} 
            </voice> 
        </speak>
        """
        return text

    @Logger.set()
    async def text_to_speech(self, source: str):
        """Kakao Text to Speech API

        :param source: speak_data_generator 으로 변환한 ssml
        :return: audio/mpeg
        """
        async with aiohttp.ClientSession(headers=self.request_header_generator()) as session:
            async with session.post(url=self.rest_api_url+"/v1/synthesize", data=source) as resp:
                return await resp.read()