from app.controller.logger import Logger


@Logger.set()
def CRC16(hash, zeroHash):
    hs = "4607"
    if len(hash) == len(hs) and hash.isalpha() == False and hash.isalnum() == True:
        zeroHash.append("101020")


@Logger.set()
def CRC16CCITT(hash, zeroHash):
    hs = "3d08"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("101040")


@Logger.set()
def FCS16(hash, zeroHash):
    hs = "0e5b"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("101060")


@Logger.set()
def CRC32(hash, zeroHash):
    hs = "b33fd057"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("102040")


@Logger.set()
def ADLER32(hash, zeroHash):
    hs = "0607cb42"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("102020")


@Logger.set()
def CRC32B(hash, zeroHash):
    hs = "b764a0d9"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("102060")


@Logger.set()
def XOR32(hash, zeroHash):
    hs = "0000003f"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("102080")


@Logger.set()
def GHash323(hash, zeroHash):
    hs = "80000000"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == True
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("103040")


@Logger.set()
def GHash325(hash, zeroHash):
    hs = "85318985"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == True
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("103020")


@Logger.set()
def DESUnix(hash, zeroHash):
    hs = "ZiY8YtDKXJwYQ"
    if len(hash) == len(hs) and hash.isdigit() == False and hash.isalpha() == False:
        zeroHash.append("104020")


@Logger.set()
def MD5Half(hash, zeroHash):
    hs = "ae11fd697ec92c7c"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("105060")


@Logger.set()
def MD5Middle(hash, zeroHash):
    hs = "7ec92c7c98de3fac"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("105040")


@Logger.set()
def MySQL(hash, zeroHash):
    hs = "63cea4673fd25f46"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("105020")


@Logger.set()
def DomainCachedCredentials(hash, zeroHash):
    hs = "f42005ec1afe77967cbc83dce1b4d714"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106025")


@Logger.set()
def Haval128(hash, zeroHash):
    hs = "d6e3ec49aa0f138a619f27609022df10"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106160")


@Logger.set()
def Haval128HMAC(hash, zeroHash):
    hs = "3ce8b0ffd75bc240fc7d967729cd6637"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106165")


@Logger.set()
def MD2(hash, zeroHash):
    hs = "08bbef4754d98806c373f2cd7d9a43c4"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106060")


@Logger.set()
def MD2HMAC(hash, zeroHash):
    hs = "4b61b72ead2b0eb0fa3b8a56556a6dca"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106120")


@Logger.set()
def MD4(hash, zeroHash):
    hs = "a2acde400e61410e79dacbdfc3413151"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106040")


@Logger.set()
def MD4HMAC(hash, zeroHash):
    hs = "6be20b66f2211fe937294c1c95d1cd4f"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106100")


@Logger.set()
def MD5(hash, zeroHash):
    hs = "ae11fd697ec92c7c98de3fac23aba525"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106020")


@Logger.set()
def MD5HMAC(hash, zeroHash):
    hs = "d57e43d2c7e397bf788f66541d6fdef9"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106080")


@Logger.set()
def MD5HMACWordpress(hash, zeroHash):
    hs = "3f47886719268dfa83468630948228f6"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106140")


@Logger.set()
def NTLM(hash, zeroHash):
    hs = "cc348bace876ea440a28ddaeb9fd3550"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106029")


@Logger.set()
def RAdminv2x(hash, zeroHash):
    hs = "baea31c728cbf0cd548476aa687add4b"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106027")


@Logger.set()
def RipeMD128(hash, zeroHash):
    hs = "4985351cd74aff0abc5a75a0c8a54115"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106180")


@Logger.set()
def RipeMD128HMAC(hash, zeroHash):
    hs = "ae1995b931cf4cbcf1ac6fbf1a83d1d3"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106185")


@Logger.set()
def SNEFRU128(hash, zeroHash):
    hs = "4fb58702b617ac4f7ca87ec77b93da8a"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106200")


@Logger.set()
def SNEFRU128HMAC(hash, zeroHash):
    hs = "59b2b9dcc7a9a7d089cecf1b83520350"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106205")


@Logger.set()
def Tiger128(hash, zeroHash):
    hs = "c086184486ec6388ff81ec9f23528727"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106220")


@Logger.set()
def Tiger128HMAC(hash, zeroHash):
    hs = "c87032009e7c4b2ea27eb6f99723454b"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106225")


@Logger.set()
def md5passsalt(hash, zeroHash):
    hs = "5634cc3b922578434d6e9342ff5913f7"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106240")


@Logger.set()
def md5saltmd5pass(hash, zeroHash):
    hs = "245c5763b95ba42d4b02d44bbcd916f1"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106260")


@Logger.set()
def md5saltpass(hash, zeroHash):
    hs = "22cc5ce1a1ef747cd3fa06106c148dfa"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106280")


@Logger.set()
def md5saltpasssalt(hash, zeroHash):
    hs = "469e9cdcaff745460595a7a386c4db0c"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106300")


@Logger.set()
def md5saltpassusername(hash, zeroHash):
    hs = "9ae20f88189f6e3a62711608ddb6f5fd"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106320")


@Logger.set()
def md5saltmd5pass(hash, zeroHash):
    hs = "aca2a052962b2564027ee62933d2382f"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106340")


@Logger.set()
def md5saltmd5passsalt(hash, zeroHash):
    hs = "de0237dc03a8efdf6552fbe7788b2fdd"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106360")


@Logger.set()
def md5saltmd5passsalt(hash, zeroHash):
    hs = "5b8b12ca69d3e7b2a3e2308e7bef3e6f"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106380")


@Logger.set()
def md5saltmd5saltpass(hash, zeroHash):
    hs = "d8f3b3f004d387086aae24326b575b23"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106400")


@Logger.set()
def md5saltmd5md5passsalt(hash, zeroHash):
    hs = "81f181454e23319779b03d74d062b1a2"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106420")


@Logger.set()
def md5username0pass(hash, zeroHash):
    hs = "e44a60f8f2106492ae16581c91edb3ba"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106440")


@Logger.set()
def md5usernameLFpass(hash, zeroHash):
    hs = "654741780db415732eaee12b1b909119"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106460")


@Logger.set()
def md5usernamemd5passsalt(hash, zeroHash):
    hs = "954ac5505fd1843bbb97d1b2cda0b98f"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106480")


@Logger.set()
def md5md5pass(hash, zeroHash):
    hs = "a96103d267d024583d5565436e52dfb3"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106500")


@Logger.set()
def md5md5passsalt(hash, zeroHash):
    hs = "5848c73c2482d3c2c7b6af134ed8dd89"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106520")


@Logger.set()
def md5md5passmd5salt(hash, zeroHash):
    hs = "8dc71ef37197b2edba02d48c30217b32"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106540")


@Logger.set()
def md5md5saltpass(hash, zeroHash):
    hs = "9032fabd905e273b9ceb1e124631bd67"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106560")


@Logger.set()
def md5md5saltmd5pass(hash, zeroHash):
    hs = "8966f37dbb4aca377a71a9d3d09cd1ac"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106580")


@Logger.set()
def md5md5usernamepasssalt(hash, zeroHash):
    hs = "4319a3befce729b34c3105dbc29d0c40"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106600")


@Logger.set()
def md5md5md5pass(hash, zeroHash):
    hs = "ea086739755920e732d0f4d8c1b6ad8d"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106620")


@Logger.set()
def md5md5md5md5pass(hash, zeroHash):
    hs = "02528c1f2ed8ac7d83fe76f3cf1c133f"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106640")


@Logger.set()
def md5md5md5md5md5pass(hash, zeroHash):
    hs = "4548d2c062933dff53928fd4ae427fc0"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106660")


@Logger.set()
def md5sha1pass(hash, zeroHash):
    hs = "cb4ebaaedfd536d965c452d9569a6b1e"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106680")


@Logger.set()
def md5sha1md5pass(hash, zeroHash):
    hs = "099b8a59795e07c334a696a10c0ebce0"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106700")


@Logger.set()
def md5sha1md5sha1pass(hash, zeroHash):
    hs = "06e4af76833da7cc138d90602ef80070"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106720")


@Logger.set()
def md5strtouppermd5pass(hash, zeroHash):
    hs = "519de146f1a658ab5e5e2aa9b7d2eec8"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("106740")


@Logger.set()
def LineageIIC4(hash, zeroHash):
    hs = "0x49a57f66bd3d5ba6abda5579c264a0e4"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
        and hash[0:2].find("0x") == 0
    ):
        zeroHash.append("107080")


@Logger.set()
def MD5phpBB3(hash, zeroHash):
    hs = "$H$9kyOtE8CDqMJ44yfn9PFz2E.L2oVzL1"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[0:3].find("$H$") == 0
    ):
        zeroHash.append("107040")


@Logger.set()
def MD5Unix(hash, zeroHash):
    hs = "$1$cTuJH0Ju$1J8rI.mJReeMvpKUZbSlY/"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[0:3].find("$1$") == 0
    ):
        zeroHash.append("107060")


@Logger.set()
def MD5Wordpress(hash, zeroHash):
    hs = "$P$BiTOhOj3ukMgCci2juN0HRbCdDRqeh."
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[0:3].find("$P$") == 0
    ):
        zeroHash.append("107020")


@Logger.set()
def MD5APR(hash, zeroHash):
    hs = "$apr1$qAUKoKlG$3LuCncByN76eLxZAh/Ldr1"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash[0:4].find("$apr") == 0
    ):
        zeroHash.append("108020")


@Logger.set()
def Haval160(hash, zeroHash):
    hs = "a106e921284dd69dad06192a4411ec32fce83dbb"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109100")


@Logger.set()
def Haval160HMAC(hash, zeroHash):
    hs = "29206f83edc1d6c3f680ff11276ec20642881243"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109200")


@Logger.set()
def MySQL5(hash, zeroHash):
    hs = "9bb2fb57063821c762cc009f7584ddae9da431ff"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109040")


@Logger.set()
def MySQL160bit(hash, zeroHash):
    hs = "*2470c0c06dee42fd1618bb99005adca2ec9d1e19"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[0:1].find("*") == 0
    ):
        zeroHash.append("109060")


@Logger.set()
def RipeMD160(hash, zeroHash):
    hs = "dc65552812c66997ea7320ddfb51f5625d74721b"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109120")


@Logger.set()
def RipeMD160HMAC(hash, zeroHash):
    hs = "ca28af47653b4f21e96c1235984cb50229331359"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109180")


@Logger.set()
def SHA1(hash, zeroHash):
    hs = "4a1d4dbc1e193ec3ab2e9213876ceb8f4db72333"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109020")


@Logger.set()
def SHA1HMAC(hash, zeroHash):
    hs = "6f5daac3fee96ba1382a09b1ba326ca73dccf9e7"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109140")


@Logger.set()
def SHA1MaNGOS(hash, zeroHash):
    hs = "a2c0cdb6d1ebd1b9f85c6e25e0f8732e88f02f96"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109220")


@Logger.set()
def SHA1MaNGOS2(hash, zeroHash):
    hs = "644a29679136e09d0bd99dfd9e8c5be84108b5fd"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109240")


@Logger.set()
def Tiger160(hash, zeroHash):
    hs = "c086184486ec6388ff81ec9f235287270429b225"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109080")


@Logger.set()
def Tiger160HMAC(hash, zeroHash):
    hs = "6603161719da5e56e1866e4f61f79496334e6a10"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109160")


@Logger.set()
def sha1passsalt(hash, zeroHash):
    hs = "f006a1863663c21c541c8d600355abfeeaadb5e4"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109260")


@Logger.set()
def sha1saltpass(hash, zeroHash):
    hs = "299c3d65a0dcab1fc38421783d64d0ecf4113448"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109280")


@Logger.set()
def sha1saltmd5pass(hash, zeroHash):
    hs = "860465ede0625deebb4fbbedcb0db9dc65faec30"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109300")


@Logger.set()
def sha1saltmd5passsalt(hash, zeroHash):
    hs = "6716d047c98c25a9c2cc54ee6134c73e6315a0ff"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109320")


@Logger.set()
def sha1saltsha1pass(hash, zeroHash):
    hs = "58714327f9407097c64032a2fd5bff3a260cb85f"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109340")


@Logger.set()
def sha1saltsha1saltsha1pass(hash, zeroHash):
    hs = "cc600a2903130c945aa178396910135cc7f93c63"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109360")


@Logger.set()
def sha1usernamepass(hash, zeroHash):
    hs = "3de3d8093bf04b8eb5f595bc2da3f37358522c9f"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109380")


@Logger.set()
def sha1usernamepasssalt(hash, zeroHash):
    hs = "00025111b3c4d0ac1635558ce2393f77e94770c5"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109400")


@Logger.set()
def sha1md5pass(hash, zeroHash):
    hs = "fa960056c0dea57de94776d3759fb555a15cae87"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("1094202")


@Logger.set()
def sha1md5passsalt(hash, zeroHash):
    hs = "1dad2b71432d83312e61d25aeb627593295bcc9a"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109440")


@Logger.set()
def sha1md5sha1pass(hash, zeroHash):
    hs = "8bceaeed74c17571c15cdb9494e992db3c263695"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109460")


@Logger.set()
def sha1sha1pass(hash, zeroHash):
    hs = "3109b810188fcde0900f9907d2ebcaa10277d10e"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109480")


@Logger.set()
def sha1sha1passsalt(hash, zeroHash):
    hs = "780d43fa11693b61875321b6b54905ee488d7760"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109500")


@Logger.set()
def sha1sha1passsubstrpass03(hash, zeroHash):
    hs = "5ed6bc680b59c580db4a38df307bd4621759324e"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109520")


@Logger.set()
def sha1sha1saltpass(hash, zeroHash):
    hs = "70506bac605485b4143ca114cbd4a3580d76a413"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109540")


@Logger.set()
def sha1sha1sha1pass(hash, zeroHash):
    hs = "3328ee2a3b4bf41805bd6aab8e894a992fa91549"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109560")


@Logger.set()
def sha1strtolowerusernamepass(hash, zeroHash):
    hs = "79f575543061e158c2da3799f999eb7c95261f07"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("109580")


@Logger.set()
def Haval192(hash, zeroHash):
    hs = "cd3a90a3bebd3fa6b6797eba5dab8441f16a7dfa96c6e641"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("110040")


@Logger.set()
def Haval192HMAC(hash, zeroHash):
    hs = "39b4d8ecf70534e2fd86bb04a877d01dbf9387e640366029"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("110080")


@Logger.set()
def Tiger192(hash, zeroHash):
    hs = "c086184486ec6388ff81ec9f235287270429b2253b248a70"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("110020")


@Logger.set()
def Tiger192HMAC(hash, zeroHash):
    hs = "8e914bb64353d4d29ab680e693272d0bd38023afa3943a41"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("110060")


@Logger.set()
def MD5passsaltjoomla1(hash, zeroHash):
    hs = "35d1c0d69a2df62be2df13b087343dc9:BeKMviAfcXeTPTlX"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[32:33].find(":") == 0
    ):
        zeroHash.append("112020")


@Logger.set()
def SHA1Django(hash, zeroHash):
    hs = "sha1$Zion3R$299c3d65a0dcab1fc38421783d64d0ecf4113448"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[0:5].find("sha1$") == 0
    ):
        zeroHash.append("113020")


@Logger.set()
def Haval224(hash, zeroHash):
    hs = "f65d3c0ef6c56f4c74ea884815414c24dbf0195635b550f47eac651a"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("114040")


@Logger.set()
def Haval224HMAC(hash, zeroHash):
    hs = "f10de2518a9f7aed5cf09b455112114d18487f0c894e349c3c76a681"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("114080")


@Logger.set()
def SHA224(hash, zeroHash):
    hs = "e301f414993d5ec2bd1d780688d37fe41512f8b57f6923d054ef8e59"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("114020")


@Logger.set()
def SHA224HMAC(hash, zeroHash):
    hs = "c15ff86a859892b5e95cdfd50af17d05268824a6c9caaa54e4bf1514"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("114060")


@Logger.set()
def SHA256(hash, zeroHash):
    hs = "2c740d20dab7f14ec30510a11f8fd78b82bc3a711abe8a993acdb323e78e6d5e"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115020")


@Logger.set()
def SHA256HMAC(hash, zeroHash):
    hs = "d3dd251b7668b8b6c12e639c681e88f2c9b81105ef41caccb25fcde7673a1132"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115120")


@Logger.set()
def Haval256(hash, zeroHash):
    hs = "7169ecae19a5cd729f6e9574228b8b3c91699175324e6222dec569d4281d4a4a"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115040")


@Logger.set()
def Haval256HMAC(hash, zeroHash):
    hs = "6aa856a2cfd349fb4ee781749d2d92a1ba2d38866e337a4a1db907654d4d4d7a"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115140")


@Logger.set()
def GOSTR341194(hash, zeroHash):
    hs = "ab709d384cce5fda0793becd3da0cb6a926c86a8f3460efb471adddee1c63793"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115060")


@Logger.set()
def RipeMD256(hash, zeroHash):
    hs = "5fcbe06df20ce8ee16e92542e591bdea706fbdc2442aecbf42c223f4461a12af"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115080")


@Logger.set()
def RipeMD256HMAC(hash, zeroHash):
    hs = "43227322be1b8d743e004c628e0042184f1288f27c13155412f08beeee0e54bf"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115160")


@Logger.set()
def SNEFRU256(hash, zeroHash):
    hs = "3a654de48e8d6b669258b2d33fe6fb179356083eed6ff67e27c5ebfa4d9732bb"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115100")


@Logger.set()
def SNEFRU256HMAC(hash, zeroHash):
    hs = "4e9418436e301a488f675c9508a2d518d8f8f99e966136f2dd7e308b194d74f9"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115180")


@Logger.set()
def SHA256md5pass(hash, zeroHash):
    hs = "b419557099cfa18a86d1d693e2b3b3e979e7a5aba361d9c4ec585a1a70c7bde4"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115200")


@Logger.set()
def SHA256sha1pass(hash, zeroHash):
    hs = "afbed6e0c79338dbfe0000efe6b8e74e3b7121fe73c383ae22f5b505cb39c886"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("115220")


@Logger.set()
def MD5passsaltjoomla2(hash, zeroHash):
    hs = "fb33e01e4f8787dc8beb93dac4107209:fxJUXVjYRafVauT77Cze8XwFrWaeAYB2"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[32:33].find(":") == 0
    ):
        zeroHash.append("116020")


@Logger.set()
def SAM(hash, zeroHash):
    hs = "4318B176C3D8E3DEAAD3B435B51404EE:B7C899154197E8A2A33121D76A240AB5"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash.islower() == False
        and hash[32:33].find(":") == 0
    ):
        zeroHash.append("116040")


@Logger.set()
def SHA256Django(hash, zeroHash):
    hs = (
        "sha256$Zion3R$9e1a08aa28a22dfff722fad7517bae68a55444bb5e2f909d340767cec9acf2c3"
    )
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[0:6].find("sha256") == 0
    ):
        zeroHash.append("117020")


@Logger.set()
def RipeMD320(hash, zeroHash):
    hs = "b4f7c8993a389eac4f421b9b3b2bfb3a241d05949324a8dab1286069a18de69aaf5ecc3c2009d8ef"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("118020")


@Logger.set()
def RipeMD320HMAC(hash, zeroHash):
    hs = "244516688f8ad7dd625836c0d0bfc3a888854f7c0161f01de81351f61e98807dcd55b39ffe5d7a78"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("118040")


@Logger.set()
def SHA384(hash, zeroHash):
    hs = "3b21c44f8d830fa55ee9328a7713c6aad548fe6d7a4a438723a0da67c48c485220081a2fbc3e8c17fd9bd65f8d4b4e6b"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("119020")


@Logger.set()
def SHA384HMAC(hash, zeroHash):
    hs = "bef0dd791e814d28b4115eb6924a10beb53da47d463171fe8e63f68207521a4171219bb91d0580bca37b0f96fddeeb8b"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("119040")


@Logger.set()
def SHA256s(hash, zeroHash):
    hs = "$6$g4TpUQzk$OmsZBJFwvy6MwZckPvVYfDnwsgktm2CckOlNJGy9HNwHSuHFvywGIuwkJ6Bjn3kKbB6zoyEjIYNMpHWBNxJ6g."
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[0:3].find("$6$") == 0
    ):
        zeroHash.append("120020")


@Logger.set()
def SHA384Django(hash, zeroHash):
    hs = "sha384$Zion3R$88cfd5bc332a4af9f09aa33a1593f24eddc01de00b84395765193c3887f4deac46dc723ac14ddeb4d3a9b958816b7bba"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == False
        and hash[0:6].find("sha384") == 0
    ):
        zeroHash.append("121020")


@Logger.set()
def SHA512(hash, zeroHash):
    hs = "ea8e6f0935b34e2e6573b89c0856c81b831ef2cadfdee9f44eb9aa0955155ba5e8dd97f85c73f030666846773c91404fb0e12fb38936c56f8cf38a33ac89a24e"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("122020")


@Logger.set()
def SHA512HMAC(hash, zeroHash):
    hs = "dd0ada8693250b31d9f44f3ec2d4a106003a6ce67eaa92e384b356d1b4ef6d66a818d47c1f3a2c6e8a9a9b9bdbd28d485e06161ccd0f528c8bbb5541c3fef36f"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("122060")


@Logger.set()
def Whirlpool(hash, zeroHash):
    hs = "76df96157e632410998ad7f823d82930f79a96578acc8ac5ce1bfc34346cf64b4610aefa8a549da3f0c1da36dad314927cebf8ca6f3fcd0649d363c5a370dddb"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("122040")


@Logger.set()
def WhirlpoolHMAC(hash, zeroHash):
    hs = "77996016cf6111e97d6ad31484bab1bf7de7b7ee64aebbc243e650a75a2f9256cef104e504d3cf29405888fca5a231fcac85d36cd614b1d52fce850b53ddf7f9"
    if (
        len(hash) == len(hs)
        and hash.isdigit() == False
        and hash.isalpha() == False
        and hash.isalnum() == True
    ):
        zeroHash.append("122080")
