import discord
from discord.ext import commands
from discord.ext.voice_recv import VoiceRecvClient, WaveSink
import os
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ 디스코드 봇 로그인 성공: {bot.user.name}')
    print('------')
    print('사용 가능 명령어:')
    print('!join  - 봇을 음성 채널로 초대')
    print('!start - 녹음 시작')
    print('!stop  - 녹음 중지 및 저장')
    print('!leave - 봇을 음성 채널에서 퇴장')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect(cls=VoiceRecvClient)
        await ctx.send(f"🎤 {channel.name} 채널에 접속했습니다.")
    else:
        await ctx.send("❌ 먼저 음성 채널에 참여해 주세요!")

@bot.command()
async def start(ctx):
    if not ctx.voice_client:
        await ctx.invoke(join)
    
    if not ctx.voice_client.is_listening():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"recording_{timestamp}.wav"
        
        # WaveSink를 사용하여 오디오 저장
        ctx.voice_client.listen(WaveSink(filename))
        await ctx.send(f"🔴 녹음을 시작합니다! (파일 이름: {filename})")
    else:
        await ctx.send("⚠️ 이미 녹음이 진행 중입니다.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_listening():
        ctx.voice_client.stop_listening()
        await ctx.send("⏹️ 녹음을 중지했습니다. 파일을 **디글루(D-gle)**에 업로드하여 요약 결과를 생성하세요.")
    else:
        await ctx.send("❌ 현재 녹음 중이 아닙니다.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 퇴장합니다.")
    else:
        await ctx.send("❌ 현재 음성 채널에 있지 않습니다.")

# 토큰 실행
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN or TOKEN == "your_token_here":
    print("❌ Error: .env 파일에 올바른 DISCORD_BOT_TOKEN을 입력해 주세요.")
else:
    bot.run(TOKEN)
