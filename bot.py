import asyncio
from playwright.async_api import async_playwright
import requests
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_alerta(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

async def verificar_ingresso():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        URLS = [
            "https://www.ticketmaster.com.br/event/bts-world-tour-arirang-dia-28",
            "https://www.ticketmaster.com.br/event/bts-world-tour-arirang-dia-30",
            "https://www.ticketmaster.com.br/event/bts-world-tour-arirang-dia-31"
        ]

        for url in URLS:
            await page.goto(url)
            await page.wait_for_timeout(5000)

            botao = await page.query_selector("button:has-text('Comprar')")

            if botao:
                await browser.close()
                return url

        await browser.close()
        return None

async def main():
    print("Bot iniciado...")
    enviar_alerta("🚀 BOT ONLINE!")

    while True:
        try:
            url = await verificar_ingresso()

            if url:
                enviar_alerta(f"🚨 INGRESSO DISPONÍVEL!\n{url}")
                print("Ingresso encontrado!")
                time.sleep(60)
            else:
                print("Nada ainda...")

        except Exception as e:
            print("Erro:", e)

        time.sleep(15)

asyncio.run(main())