import feedparser
import telegram
import asyncio
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Ma'lumotlar
RSS_URL = "https://filmsevar.blogspot.com/feeds/posts/default?alt=rss"
TOKEN = "7781935889:AAGY1F4yhgaWSO68SOk1aCr5Z5vKq7u_l0g"
CHAT_ID = "@kino_sevarr"

# Render uchun kichik veb-server (Xatolik chiqmasligi uchun)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_health_check():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

async def check_posts():
    last_post_link = ""
    bot = telegram.Bot(token=TOKEN)
    print("Bot muvaffaqiyatli ishga tushdi...")
    
    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            if feed.entries:
                latest_post = feed.entries[0]
                link = latest_post.link
                title = latest_post.title
                
                if link != last_post_link:
                    if last_post_link != "":
                        message = f"🎬 Yangi maqola chiqdi!\n\n{title}\n\n🔗 O'qish: {link}"
                        await bot.send_message(chat_id=CHAT_ID, text=message)
                        print(f"Yuborildi: {title}")
                    last_post_link = link
        except Exception as e:
            print(f"Xatolik: {e}")
        
        await asyncio.sleep(300)

if __name__ == "__main__":
    # Veb-serverni alohida oqimda yoqish
    threading.Thread(target=run_health_check, daemon=True).start()
    # Botni ishga tushirish
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(check_posts())
