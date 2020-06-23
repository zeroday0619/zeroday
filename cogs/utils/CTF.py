import base64
import binascii
import codecs
import discord
import collections
import hashlib
import string

from .ext.hashDec import HashDetection
from discord.ext import commands


class CTF(commands.Cog):
    """ctf 관련 기능"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='enc')
    async def encode(self, context):
        """
        ```markdown
        Encode
        ----------------------
        |   Type   | aliases |
        |:--------:|:-------:|
        |  base85  |   b85   |
        |  base64  |   b64   |
        |  base32  |   b32   |
        |  rot13   |   r13   |
        | ascii85  |   a85   |
        |  hex     |  None   |
        ```
        """
        if context.invoked_subcommand is None:
            help_cmd = self.bot.get_command('help')
            await context.invoke(help_cmd, 'encode')

    @commands.group(name="dec")
    async def decode(self, context):
        """
        ```markdown
        decode
        ----------------------
        |   Type   | aliases |
        |:--------:|:-------:|
        |  base85  |   b85   |
        |  base64  |   b64   |
        |  base32  |   b32   |
        |  rot13   |   r13   |
        | ascii85  |   a85   |
        |  hex     |  None   |
        ```
        """
        if context.invoked_subcommand is None:
            help_cmd = self.bot.get_command('help')
            await context.invoke(help_cmd, 'decode')

    @staticmethod
    async def encryptout(context, convert, input):
        if len(input) > 1900:
            return await context.send(f"**{context.author.name}** 결과가 최대 출력 제한을 초과했습니다.")

        try:
            await context.send(f"**{convert}**```fix\n{input.decode('UTF-8')}```")
        except AttributeError:
            await context.send(f"**{convert}**```fix\n{input}```")

    @encode.command(name="base32", aliases=["b32"])
    async def encode_base32(self, context, *, input: commands.clean_content):
        """base32 인코딩"""
        await self.encryptout(
            context, "Text -> base32", base64.b32encode(input.encode('UTF-8'))
        )

    @decode.command(name="base32", aliases=["b32"])
    async def decode_base32(self, context, *, input: str):
        """base32 디코딩"""
        try:
            await self.encryptout(context, "base32 -> Text", base64.b32decode(input.encode('UTF-8')))
        except Exception:
            await context.send("유효하지 않은 base32")

    @encode.command(name="base64", aliases=["b64"])
    async def encode_base64(self, context, *, input: commands.clean_content):
        """base64 인코딩"""
        await self.encryptout(
            context, "Text -> base64", base64.urlsafe_b64encode(input.encode('UTF-8'))
        )

    @decode.command(name="base64", aliases=["b64"])
    async def decode_base64(self, context, *, input: str):
        """base64 디코딩"""
        try:
            await self.encryptout(context, "base64 -> Text", base64.urlsafe_b64decode(input.encode('UTF-8')))
        except Exception:
            await context.send("유효하지 않은 base64...")

    @encode.command(name="rot13", aliases=["r13"])
    async def encode_rot13(self, context, *, input: commands.clean_content):
        """rot13 인코딩"""
        await self.encryptout(
            context, "Text -> rot13", codecs.decode(input, 'rot_13')
        )

    @decode.command(name="rot13", aliases=["r13"])
    async def decode_rot13(self, context, *, input: str):
        """rot13 디코딩"""
        try:
            await self.encryptout(context, "rot13 -> Text", codecs.decode(input, 'rot_13'))
        except Exception:
            await context.send("유효하지 않은 rot13...")

    @encode.command(name="hex")
    async def encode_hex(self, context, *, input: commands.clean_content):
        """hex 인코딩"""
        await self.encryptout(
            context, "Text -> hex",
            binascii.hexlify(input.encode('UTF-8'))
        )

    @decode.command(name="hex")
    async def decode_hex(self, context, *, input: str):
        """hex 디코딩"""
        try:
            await self.encryptout(context, "hex -> Text", binascii.unhexlify(input.encode('UTF-8')))
        except Exception:
            await context.send("유효하지 않은 hex...")

    @encode.command(name="base85", aliases=["b85"])
    async def encode_base85(self, context, *, input: commands.clean_content):
        """base85 인코딩"""
        await self.encryptout(
            context, "Text -> base85",
            base64.b85encode(input.encode('UTF-8'))
        )

    @decode.command(name="base85", aliases=["b85"])
    async def decode_base85(self, context, *, input: str):
        """base85 디코딩"""
        try:
            await self.encryptout(context, "base85 -> Text", base64.b85decode(input.encode('UTF-8')))
        except Exception:
            await context.send("유효하지 않은 base85...")

    @encode.command(name="ascii85", aliases=["a85"])
    async def encode_ascii85(self, context, *, input: commands.clean_content):
        """ASCII85 인코딩"""
        await self.encryptout(
            context, "Text -> ASCII85",
            base64.a85encode(input.encode('UTF-8'))
        )

    @decode.command(name="ascii85", aliases=["a85"])
    async def decode_ascii85(self, context, *, input: str):
        """ASCII85 디코딩"""
        try:
            await self.encryptout(context, "ASCII85 -> Text", base64.a85decode(input.encode('UTF-8')))
        except Exception:
            await context.send("유효하지 않은 ASCII85...")

    @commands.group(name="util")
    async def _ctf(self, context):
        """
        ```markdown
        String Util
        ----------------------
        |   Type   | aliases |
        |:--------:|:-------:|
        |   char   |   None  |
        |    wc    |   None  |
        |   rev    |   None  |
        |   rot    |   r13   |
        |  encbin  |   None  |
        |counteach |   cth   |
        | atbash   |   None  |
        | decbin   |   None  |
        ```
        """
        if context.invoked_subcommand is None:
            help_cmd = self.bot.get_command('help')
            await context.invoke(help_cmd, 'ctf')

    @_ctf.command(aliases=['char'])
    async def characters(self, context, *, input: str):
        """char"""
        await context.send(len(input))

    @_ctf.command(aliases=['wc'])
    async def wordcount(self, context, *args):
        """wc"""
        await context.send(len(args))

    @_ctf.command(aliases=['rev'])
    async def reverse(self, context, *, input: str):
        """rev"""
        await context.send(input[::(- 1)])

    @_ctf.command(name="counteach", aliases=['cth'])
    async def _counteach(self, context, *, input: str):
        """counteach"""
        count = {}
        
        for char in input:
            if char in count.keys():
                count[char] += 1
            else:
                count[char] = 1
        
        await context.send(str(count))

    @_ctf.command()
    async def rot(self, context, *, input: str, direction=None):
        """rot"""
        allrot = ''
        
        for i in range(0, 26):
            upper = collections.deque(string.ascii_uppercase)
            lower = collections.deque(string.ascii_lowercase)
            
            upper.rotate((- i))
            lower.rotate((- i))
            
            upper = ''.join(list(upper))
            lower = ''.join(list(lower))
            translated = input.translate(str.maketrans(string.ascii_uppercase, upper)).translate(str.maketrans(string.ascii_lowercase, lower))
            allrot += '{}: {}\n'.format(i, translated)
        
        await context.send(f"{allrot}")

    @_ctf.command()
    async def atbash(self, context, *, input: str):
        """atbash"""
        normal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        changed = 'zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA'
        trans = str.maketrans(normal, changed)
        atbashed = input.translate(trans)
        await context.send(atbashed)

    @_ctf.command(aliases=['encbin'])
    async def encode_binary(self, context, *, input: str):
        """encode_binary"""
        await self.encryptout(
            context, "Text -> binary",
            bin(int.from_bytes(input.encode(), 'big')).replace('b', '')
        )

    @_ctf.command(aliases=['decbin'])
    async def decode_binary(self, context, *, input: str):
        """decode_binary"""
        data = int(input.replace(" ", ""), 2),
        await self.encryptout(
            context, "binary -> text",
            data.to_bytes((data.bit_length() + 7) // 8, 'big').decode()
        )

    @commands.group()
    async def crypto(self, context):
        """
        ```markdown
        crypto & hash
        ---------------------------
        |   Type        | aliases |
        |:-------------:|:-------:|
        |  hash_detect  |   hdt   |
        |     md5       |  None   |
        |     sha1      |  None   |
        |    sha224     |  None   |
        |    sha256     |  None   |
        |    sha384     |  None   |
        |    sha512     |  None   |
        ```
        """
        if context.invoked_subcommand is None:
            help_cmd = self.bot.get_command('help')
            await context.invoke(help_cmd, 'crypto')

    @crypto.command(name="hash_detect", aliases=['hdt', 'hashtype', '해시타입'])
    async def hash_dectected(self, context, *, args):
        """hash type detection"""
        response = await HashDetection(args)
        embed = discord.Embed(
            title="hash type detection",
            description="hash encrypt type Tools BETA 1.0 ",
            color=0x44d5bb
        )
        embed.add_field(name="Result :", value=str(response))
        await context.send(
            context.author.mention,
            embed=embed
        )

    @crypto.command(name="md5")
    async def _md5(self, context,*,arg):
        """md5"""
        try:
            _md5_hash = hashlib.md5()
            _hex = _md5_hash.update(arg.encode())
            _hex = _md5_hash.hexdigest()
            await self.encryptout(
                context, "text >> md5",
                _hex
            )
        except Exception as Ex:
            await context.send("Error: "+str(Ex))

    @crypto.command(name="sha1")
    async def _sha1(self, context,* ,arg):
        """sha1"""
        try:
            sha_one = hashlib.sha1(arg.encode()).hexdigest()
            await self.encryptout(
                context, "text >> sha1",
                sha_one
            )
        except Exception as Ex:
            await context.send("Error: "+str(Ex))

    @crypto.command(name="sha224")
    async def _sha224(self, context,*, arg):
        """sha224"""
        try:
            sha224 = hashlib.sha224(arg.encode()).hexdigest()
            await self.encryptout(
                context, "text >> sha224",
                sha224
            )
        except Exception as Ex:
            await context.send("Error: "+str(Ex))

    @crypto.command(name="sha256")
    async def _sha256(self, context,*, arg):
        """sha256"""
        try:
            sha256 = hashlib.sha256(arg.encode()).hexdigest()

            await self.encryptout(
                context, "text >> sha256",
                sha256
            )
        except Exception as Ex:
            await context.send("Error: "+str(Ex))

    @crypto.command(name="sha384")
    async def _sha384(self, context,*, arg):
        """sha384"""
        try:
            sha384 = hashlib.sha384(arg.encode()).hexdigest()
            await self.encryptout(
                context, "text >> sha384",
                sha384
            )
        except Exception as Ex:
            await context.send("Error: "+str(Ex))
    
    @crypto.command(name="sha512")
    async def _sha512(self, context,*, arg):
        """sha512"""
        try:
            sha512 = hashlib.sha512(arg.encode()).hexdigest()

            await self.encryptout(
                context, "text >> sha512",
                sha512
            )

        except Exception as Ex:
            await context.send("Error: "+str(Ex))