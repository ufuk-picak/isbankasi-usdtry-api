from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()  # uvicorn main:app diye arayacak

def get_usd_try():
    url = "https://www.isbank.com.tr/en/foreign-exchange-rates"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code != 200:
            return {"error": "Siteye erişilemiyor"}
    except Exception as e:
        return {"error": str(e)}

    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 2 and "USD" in cols[0].text:
            buy = cols[1].text.strip()
            sell = cols[2].text.strip()
            return {"buy": buy, "sell": sell}

    return {"error": "USD bulunamadı"}

# API endpoint
@app.get("/usdtry")
def usd_try():
    return get_usd_try()