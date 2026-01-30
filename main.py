import feedparser
import telegram
import asyncio
import os

# Ma'lumotlar
RSS_URL = "https://filmsevar.blogspot.com/feeds/posts/default?alt=rss"
TOKEN = "7781935889:AAGY1F4yhgaWSO68SOk1aCr5Z5vKq7u_l0g"
CHAT_ID = "@kino_sevarr"
DB_FILE = "last_link.txt"

async def main():
    bot = telegram.Bot(token=TOKEN)
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print("Maqolalar topilmadi.")
        return

    latest_post = feed.entries[0]
    title = latest_post.title
    link = latest_post.link

    # Avval yuborilgan linkni tekshirish
    last_sent_link = ""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            last_sent_link = f.read().strip()

    # Agar yangi link bo'lsa, xabar yuboramiz
    if link != last_sent_link:
        message = f"🎬 *Yangi maqola chiqdi!*\n\n*{title}*\n\n🔗 O'qish: {link}"
        try:
            await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
            print(f"Yuborildi: {title}")
            
            # Yuborilgan linkni saqlab qo'yamiz
            with open(DB_FILE, "w") as f:
                f.write(link)
        except Exception as e:
            print(f"Xato: {e}")
    else:
        print("Bu maqola allaqachon yuborilgan.")

if __name__ == "__main__":
    asyncio.run(main())
