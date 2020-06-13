from .hash_ext import algorithms
from .hash_ext.hash_data import ADLER32, CRC16, CRC16CCITT, CRC32, CRC32B, DESUnix, DomainCachedCredentials,\
    FCS16, GHash323, GHash325, GOSTR341194, Haval128, Haval128HMAC, Haval160, Haval160HMAC, Haval192, Haval192HMAC, Haval224,\
    Haval224HMAC, Haval256, Haval256HMAC, LineageIIC4, MD2, MD2HMAC, MD4, MD4HMAC, MD5, MD5APR, MD5HMAC, MD5HMACWordpress, \
    MD5phpBB3, MD5Unix, MD5Wordpress, MD5Half, MD5Middle, MD5passsaltjoomla1, MD5passsaltjoomla2, MySQL, MySQL5, MySQL160bit, \
    NTLM, RAdminv2x, RipeMD128, RipeMD128HMAC, RipeMD160, RipeMD160HMAC, RipeMD256, RipeMD256HMAC, RipeMD320, RipeMD320HMAC, \
    SAM, SHA1, SHA1Django, SHA1HMAC, SHA1MaNGOS, SHA1MaNGOS2, SHA224, SHA224HMAC, SHA256, SHA256s, SHA256Django, SHA256HMAC, \
    SHA256md5pass, SHA256sha1pass, SHA384, SHA384Django, SHA384HMAC, SHA512, SHA512HMAC, SNEFRU128, SNEFRU128HMAC, SNEFRU256,\
    SNEFRU256HMAC, Tiger128, Tiger128HMAC, Tiger160, Tiger160HMAC, Tiger192, Tiger192HMAC, Whirlpool, WhirlpoolHMAC, XOR32, \
    md5passsalt, md5saltmd5pass, md5saltpass, md5saltpasssalt, md5saltpassusername, md5saltmd5pass, md5saltmd5passsalt, \
    md5saltmd5passsalt, md5saltmd5saltpass, md5saltmd5md5passsalt, md5username0pass, md5usernameLFpass, md5usernamemd5passsalt,\
    md5md5pass, md5md5passsalt, md5md5passmd5salt, md5md5saltpass, md5md5saltmd5pass, md5md5usernamepasssalt, md5md5md5pass,\
    md5md5md5md5pass, md5md5md5md5md5pass, md5sha1pass, md5sha1md5pass, md5sha1md5sha1pass, md5strtouppermd5pass, sha1passsalt,\
    sha1saltpass, sha1saltmd5pass, sha1saltmd5passsalt, sha1saltsha1pass, sha1saltsha1saltsha1pass, sha1usernamepass, sha1usernamepasssalt,\
    sha1md5pass, sha1md5passsalt, sha1md5sha1pass, sha1sha1pass, sha1sha1passsalt, sha1sha1passsubstrpass03, sha1sha1saltpass,\
    sha1sha1sha1pass, sha1strtolowerusernamepass


async def HashDetection(code):
    zeroHash = []
    h = code
    ADLER32(h, zeroHash); CRC16(h, zeroHash); CRC16CCITT(h, zeroHash);  CRC32(h, zeroHash);  CRC32B(h, zeroHash);  DESUnix(h, zeroHash);  DomainCachedCredentials(h, zeroHash);  FCS16(h, zeroHash);  GHash323(h, zeroHash);  GHash325(h, zeroHash);  GOSTR341194(h, zeroHash);  Haval128(h, zeroHash);  Haval128HMAC(h, zeroHash);  Haval160(h, zeroHash);  Haval160HMAC(h, zeroHash);  Haval192(h, zeroHash);  Haval192HMAC(h, zeroHash);  Haval224(h, zeroHash);  Haval224HMAC(h, zeroHash);  Haval256(h, zeroHash);  Haval256HMAC(h, zeroHash);  LineageIIC4(h, zeroHash);  MD2(h, zeroHash);  MD2HMAC(h, zeroHash);  MD4(h, zeroHash);  MD4HMAC(h, zeroHash);  MD5(h, zeroHash);  MD5APR(h, zeroHash);  MD5HMAC(h, zeroHash);  MD5HMACWordpress(h, zeroHash);  MD5phpBB3(h, zeroHash);  MD5Unix(h, zeroHash);  MD5Wordpress(h, zeroHash);  MD5Half(h, zeroHash);  MD5Middle(h, zeroHash);  MD5passsaltjoomla1(h, zeroHash);  MD5passsaltjoomla2(h, zeroHash);  MySQL(h, zeroHash);  MySQL5(h, zeroHash);  MySQL160bit(h, zeroHash);  NTLM(h, zeroHash);  RAdminv2x(h, zeroHash);  RipeMD128(h, zeroHash);  RipeMD128HMAC(h, zeroHash);  RipeMD160(h, zeroHash);  RipeMD160HMAC(h, zeroHash);  RipeMD256(h, zeroHash);  RipeMD256HMAC(h, zeroHash);  RipeMD320(h, zeroHash);  RipeMD320HMAC(h, zeroHash);  SAM(h, zeroHash);  SHA1(h, zeroHash);  SHA1Django(h, zeroHash);  SHA1HMAC(h, zeroHash);  SHA1MaNGOS(h, zeroHash);  SHA1MaNGOS2(h, zeroHash);  SHA224(h, zeroHash);  SHA224HMAC(h, zeroHash);  SHA256(h, zeroHash);  SHA256s(h, zeroHash);  SHA256Django(h, zeroHash);  SHA256HMAC(h, zeroHash);  SHA256md5pass(h, zeroHash);  SHA256sha1pass(h, zeroHash);  SHA384(h, zeroHash);  SHA384Django(h, zeroHash);  SHA384HMAC(h, zeroHash);  SHA512(h, zeroHash);  SHA512HMAC(h, zeroHash);  SNEFRU128(h, zeroHash);  SNEFRU128HMAC(h, zeroHash);  SNEFRU256(h, zeroHash);  SNEFRU256HMAC(h, zeroHash);  Tiger128(h, zeroHash);  Tiger128HMAC(h, zeroHash);  Tiger160(h, zeroHash);  Tiger160HMAC(h, zeroHash);  Tiger192(h, zeroHash);  Tiger192HMAC(h, zeroHash);  Whirlpool(h, zeroHash);  WhirlpoolHMAC(h, zeroHash);  XOR32(h, zeroHash);  md5passsalt(h, zeroHash);  md5saltmd5pass(h, zeroHash);  md5saltpass(h, zeroHash);  md5saltpasssalt(h, zeroHash);  md5saltpassusername(h, zeroHash);  md5saltmd5pass(h, zeroHash);  md5saltmd5passsalt(h, zeroHash);  md5saltmd5passsalt(h, zeroHash);  md5saltmd5saltpass(h, zeroHash);  md5saltmd5md5passsalt(h, zeroHash);  md5username0pass(h, zeroHash);  md5usernameLFpass(h, zeroHash);  md5usernamemd5passsalt(h, zeroHash);  md5md5pass(h, zeroHash);  md5md5passsalt(h, zeroHash);  md5md5passmd5salt(h, zeroHash);  md5md5saltpass(h, zeroHash);  md5md5saltmd5pass(h, zeroHash);  md5md5usernamepasssalt(h, zeroHash);  md5md5md5pass(h, zeroHash);  md5md5md5md5pass(h, zeroHash);  md5md5md5md5md5pass(h, zeroHash);  md5sha1pass(h, zeroHash);  md5sha1md5pass(h, zeroHash);  md5sha1md5sha1pass(h, zeroHash);  md5strtouppermd5pass(h, zeroHash);  sha1passsalt(h, zeroHash);  sha1saltpass(h, zeroHash);  sha1saltmd5pass(h, zeroHash);  sha1saltmd5passsalt(h, zeroHash);  sha1saltsha1pass(h, zeroHash);  sha1saltsha1saltsha1pass(h, zeroHash);  sha1usernamepass(h, zeroHash);  sha1usernamepasssalt(h, zeroHash);  sha1md5pass(h, zeroHash);  sha1md5passsalt(h, zeroHash);  sha1md5sha1pass(h, zeroHash);  sha1sha1pass(h, zeroHash);  sha1sha1passsalt(h, zeroHash);  sha1sha1passsubstrpass03(h, zeroHash);  sha1sha1saltpass(h, zeroHash);  sha1sha1sha1pass(h, zeroHash);  sha1strtolowerusernamepass(h, zeroHash);

    if len(zeroHash) == 0:
        Error: str = str("\n Not Found.")
        return Error
    elif len(zeroHash) > 2:
        zeroHash.sort()
        res = str('[+]') + str(algorithms[zeroHash[0]]) + "\n" + str('[+]') + str(algorithms[zeroHash[1]])
        return res
    else:
        return "Error"