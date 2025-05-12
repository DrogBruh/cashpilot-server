from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import traceback

app = Flask(__name__)

@app.route("/credit-offers")
def get_credit_offers():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless=new")  # new headless для Render

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get("https://www.sberbank.com/ru/person/credits/money")

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card__factoids"))
        )

        card_elements = driver.find_elements(By.CLASS_NAME, "product-card__factoids")
        offers = []

        for card in card_elements:
            factoids = card.find_elements(By.CLASS_NAME, "factoid")
            min_amount = ""
            term = ""

            for f in factoids:
                label = f.text.lower()
                if "сумма" in label:
                    min_amount = f.find_element(By.TAG_NAME, "h3").text
                if "срок" in label:
                    term = f.find_element(By.TAG_NAME, "h3").text

            if min_amount or term:
                offers.append({
                    "bankName": "Сбербанк",
                    "minAmount": min_amount,
                    "term": term
                })

        driver.quit()
        return jsonify(offers)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)