import discord
from discord.ext import commands
import os
import platform
import asyncio
from datetime import datetime
from dotenv import load_dotenv

try:
    from discord.ext.voice_recv import VoiceRecvClient, WaveSink
except ImportError:
    print("⚠️ VoiceRecvClient를 불러올 수 없습니다. 'pip install discord-ext-voice-recv' 명령어로 설치해주세요.")

# .env 로드
load_dotenv()

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")
if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

# Opus 라이브러리 설정
def load_opus_lib():
    if discord.opus.is_loaded():
        return True
    
    # OS별 라이브러리 파일명 설정
    system = platform.system()
    if system == "Darwin":  # macOS
        lib_name = "libopus.dylib"
    elif system == "Linux":
        lib_name = "libopus.so.0"
    else:
        lib_name = "libopus.so"

    # 1. 시스템 기본 경로에서 시도
    try:
        discord.opus.load_opus(lib_name)
        print(f"✅ 시스템 {lib_name} 로드 성공")
        return True
    except:
        pass

    # 2. 로컬 bin 폴더에서 시ed
    local_opus_path = os.path.join(BASE_DIR, "bin/opus-1.4/dist/lib", lib_name)
    if os.path.exists(local_opus_path):
        try:
            discord.opus.load_opus(local_opus_path)
            print(f"✅ 로컬 {lib_name} 로드 성공: {local_opus_path}")
            return True
        except Exception as e:
            print(f"⚠️ 로컬 {lib_name} 로드 실패: {e}")
    
    # 3. 흔한 리눅스 경로들 시도
    if system == "Linux":
        linux_paths = ["/usr/lib/x86_64-linux-gnu/libopus.so.0", "/usr/lib/libopus.so.0"]
        for p in linux_paths:
            if os.path.exists(p):
                try:
                    discord.opus.load_opus(p)
                    print(f"✅ 리눅스 경로 {p} 로드 성공")
                    return True
                except:
                    continue
                    
    print("❌ Opus 라이브러리를 찾을 수 없습니다. 음성 기능을 사용할 수 없을 수 있습니다.")
    return False

load_opus_lib()

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ 디스코드 봇 로그인 성공: {bot.user.name}')
    print('------')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            await channel.connect(cls=VoiceRecvClient)
            await ctx.send(f"🎤 {channel.name} 접속 성공!")
        except Exception as e:
            await ctx.send(f"❌ 접속 실패: {e}")
    else:
        await ctx.send("❌ 음성 채널에 먼저 들어가 주세요!")

@bot.command()
async def start(ctx):
    if not ctx.voice_client:
        await ctx.invoke(join)
    
    if ctx.voice_client and not ctx.voice_client.is_listening():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = os.path.join(RECORDINGS_DIR, f"recording_{timestamp}.wav")
        
        ctx.voice_client.listen(WaveSink(filename))
        await ctx.send(f"🔴 녹음을 시작합니다! (파일: {os.path.basename(filename)})")
    elif ctx.voice_client:
        await ctx.send("⚠️ 이미 녹음이 진행 중입니다.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_listening():
        ctx.voice_client.stop_listening()
        await ctx.send("⏹️ 녹음을 중지했습니다. 파일을 요약하려면 'process_minutes.py'를 실행하세요.")
    else:
        await ctx.send("❌ 현재 녹음 중이 아닙니다.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 퇴장합니다.")
    else:
        await ctx.send("❌ 음성 채널에 있지 않습니다.")

# 실행
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_BOT_TOKEN이 .env에 없습니다.")
