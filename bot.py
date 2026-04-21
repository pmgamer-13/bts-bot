import asyncio
from playwright.async_api import async_playwright
import requests
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URLS = [
    "https://www.ticketmaster.com.br/event/venda-geral-bts-world-tour-arirang-28-10",
    "https://www.ticketmaster.com.br/event/venda-geral-bts-world-tour-arirang-30-10",
    "https://www.ticketmaster.com.br/event/venda-geral-bts-world-tour-arirang-31-10"
]

def enviar_alerta(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data, timeout=5)

async def checar_url(browser, url):
    page = await browser.new_page()
    await page.goto(url)
    await page.wait_for_load_state("domcontentloaded")

    botao = await page.query_selector("button:has-text('Comprar')")
    await page.close()

    return url if botao else None

async def main():
    print("Bot iniciado...")
    enviar_alerta("🚀 BOT ONLINE")

    ultimo_alerta = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        while True:
            try:
                tasks = [checar_url(browser, url) for url in URLS]
                resultados = await asyncio.gather(*tasks)

                url_encontrada = None
                for r in resultados:
                    if r:
                        url_encontrada = r
                        break

                if url_encontrada:
                    if url_encontrada != ultimo_alerta:
                        enviar_alerta(f"🚨 INGRESSO DISPONÍVEL!\n{url_encontrada}")
                        print("Ingresso encontrado!")
                        ultimo_alerta = url_encontrada

                    await asyncio.sleep(25)
                else:
                    print("Nada ainda...")

            except Exception as e:
                print("Erro:", e)

            await asyncio.sleep(15)

asyncio.run(main())