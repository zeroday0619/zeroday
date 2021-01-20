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
            r"(ㅇㅂ|일(간|)베(스트|))",
            r"((시발)(?!역)|((시|씨|쓰|ㅅ|ㅆ)([0-9]+|\W+|)(블|벌|발|빨|뻘|ㅂ|ㅃ))(!시발))",
            r"((씨|쓰|ㅅ|ㅆ|(?i)si)([0-9]+|\W+)(블|벌|발|빨|뻘|ㅂ|ㅃ|(?i)bal))",
            r"((?i)(sibal|tlqkf))",
            r"((병|빙|븅|등|ㅂ)([0-9]+|\W+|)(신|싄|ㅅ)|ㅄ)",
            r"((?i)qudtls)",
            r"((염|옘)병)",
            r"(빡대가리|아가리|아가리닫|아닫|아가리닫아|틀딱|저능아|정박아|정신병자)",
            r"(놈|년|새끼)",
            r"((뭔|)개(소리|솔))",
            r"((급식|학식)충)",
            r"((빠|바|ba|ば|バ)(카|까|ka|か|カ))",
            r"(?i)((your)([0-9]+|\W+|)(mom|mother))",
            r"((너|느(그|)|니)([0-9]+|\W+|)(금|애미|엄마|금마|검마))",
            r"((?i)(sl|sm(rm|)|sj)([0-9]+|\W+|)(doal|rmaak|djaak))",
            r"((?i)(느금|smrma))",
            r"((?i)(your(\W+|))(father|dad))",
            r"((너|느(그|))(\W+|)(개비|가빠|아빠|애비|아비))",
            r"((?i)(sl|sm(rm|))(\W+|)(doql|dkql|rkQk))",
            r"(((MC|노)무|뇌물)현)",
            r"(노(알라|운지))",
            r"(이기|언냐|엑윽엑엑|레이디가카|땅크)",
            r"(운지(?!법)(?!버섯))",
            r"((중력|운지)절)",
            r"((?i)fuck)",
            r"((뻑|뻒|뻐)(큐|유))"          
        ]
    
    @staticmethod
    def cleanText(text: str) -> str:
        processed_text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
        return processed_text
    
    async def suicide(self, source: str):
        pt = re.compile(r"(자살)")
        if bool(pt.fullmatch(self.cleanText(source))):
            return "힘든 일이 있군요. 우리 같이 얘기해요. 당신을 도와줄 수 있는 사람이 많아요."\
            + "한국자살예방협회 24시간 자살예방상담전화 1577-0199. " \
            + "삶의 희망이 보이지 않을때 고민하지 말고 연락주세요."
        else:
            return source

    async def check(self, source: str):
        for i in range(0, len(self.database)):
            pt = re.compile(self.database[i])
            if bool(pt.fullmatch(self.cleanText(source))):
                return True
        return False

