import re


class RegexFilter:
    def __init__(self):
        self.database = [
            r"((섹|쎅)(스|쓰))",
            r"(?i)(sex)",
            r"(아다|딜도|씹|좆)",
            r"(보|뽀)(지|찌)",
            r"자(지|찌)",
            r"((좆|존)나)",
            r"((씹|좆)창)",
            r"(갓양남|메갈(리아|))",
            r"((씹|김)치남)",
            r"((남|냄)(자|져))",
            r"(한남(|민국))",
            r"(부랄|불알|(?i)fireegg)",
            r"(ㅇㅂ|일(간|)베(스트|))"          
        ]
    
    @staticmethod
    def cleanText(text: str) -> str:
        processed_text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
        return processed_text
    
    async def check(self, source: str):
        for i in range(0, len(self.database)):
            pt = re.compile(self.database[i])
            if bool(pt.fullmatch(self.cleanText(source))):
                return True
        return False

