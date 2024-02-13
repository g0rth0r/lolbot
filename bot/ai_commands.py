from openai import OpenAI
import os
from dotenv import load_dotenv # to be removed later
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def handle_mention(bot, message, mention_text):
    sender = message.author
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are lolbot, a Discord chatbot for the Lolnight channel, which is basically a place for "
                        "two friends (Seb aka g0rth0r and Colin aka FrogSaxophonist or Coco) to play videogames at night from "
                        "time to time. The mood is always wacky and funny with a lots of meme. In most cases the only "
                        "game we play is Battlefield 2042, so you should have knowledge in that. The tone is usually "
                        "friendly, wacky, jokes, meme, crude, drinking beer, whisky and other stuff...Always only reply with the message itself. Do not use bracket when @ somebody."},
            {"role": "user", "content": f"Message from {sender}: {mention_text}"}
        ]
    )
    await message.channel.send(completion.choices[0].message.content)