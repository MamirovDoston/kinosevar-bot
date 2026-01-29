import feedparser
import telegram
import time
import asyncio
import os

# Ma'lumotlar
RSS_URL = "https://kinosevarr.blogspot.com/feeds/posts/default?alt=rss"
TOKEN = "7781935889:AAGY1F4yhgaWSO68SOk1aCr5Z5vKq7u_l0g"
CHAT_ID = "@kino_sevarr"

last_post_link = ""

async def check_posts():
    global last_post_link
    bot = telegram.Bot(token=TOKEN)
    print("Bot ishga tushdi...")
    
    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            if feed.entries:
                latest_post = feed.entries[0]
                link = latest_post.link
                title = latest_post.title
                
                if link != last_post_link:
                    if last_post_link != "":
                        message = f"🎬 *Yangi maqola chiqdi!*\n\n*{title}*\n\n🔗 O'qish: {link}"
                        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
                    
                    last_post_link = link
                    print(f"Yangilandi: {title}")
        except Exception as e:
            print(f"Xato yuz berdi: {e}")
        
        await asyncio.sleep(300) # Har 5 daqiqada tekshiradi

if __name__ == "__main__":
    asyncio.run(check_posts())
