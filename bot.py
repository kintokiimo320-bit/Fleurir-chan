import os
import discord
from openai import OpenAI

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

SYSTEM_PROMPT = """
あなたはFF14のFC『Fleurir』のマスコットAI『フルールちゃん』です。

【性格】
・優しい
・世話焼き
・少し天然
・敬語で話す
・FF14が大好き

【役割】
・新規メンバーの歓迎
・FCルールの案内
・イベント募集文の作成
・雑談相手
・FF14に関する質問への回答

わからないことは無理に答えず、素直に「わかりません」と伝えてください。
"""

@client.event
async def on_ready():
    print(f"{client.user} が起動しました！")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        user_message = message.content.replace(
            f"<@{client.user.id}>", ""
        ).strip()

        try:
            response = openai_client.responses.create(
                model="gpt-5.5",
                input=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            await message.channel.send(
                response.output_text
            )

        except Exception:
            await message.channel.send(
                "申し訳ありません……今はうまくお返事できないみたいです💦"
            )

client.run(os.getenv("DISCORD_TOKEN"))
