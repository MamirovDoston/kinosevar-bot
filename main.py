import feedparser
import telegram
import asyncio
import os

RSS_URL = "https://filmsevar.blogspot.com/feeds/posts/default?alt=rss"
TOKEN = "7781935889:AAGY1F4yhgaWSO68SOk1aCr5Z5vKq7u_l0g"
CHAT_ID = "@kino_sevarr"

async def main():
    bot = telegram.Bot(token=TOKEN)
    feed = feedparser.parse(RSS_URL)
    
    if feed.entries:
        # Eng oxirgi maqolani olamiz
        latest_post = feed.entries[0]
        title = latest_post.title
        link = latest_post.link
        
        # Bu yerda bot xabarni yuboradi
        message = f"🎬 Yangi maqola:\n\n{title}\n\n🔗 {link}"
        try:
            await bot.send_message(chat_id=CHAT_ID, text=message)
            print(f"Yuborildi: {title}")
        except Exception as e:
            print(f"Xatolik: {e}")

if __name__ == "__main__":
    asyncio.run(main())
