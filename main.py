from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "API is alive"}

@app.get("/api/usd-try")
def get_usd_try_api():
    url = "https://www.isbank.com.tr/en/foreign-exchange-rates"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 2:
                if "USD" in cols[0].text:
                    return {
                        "buy": cols[1].text.strip(),
                        "sell": cols[2].text.strip()
                    }
    except Exception as e:
        return {"error": str(e)}

    return {"error": "USD not found"}