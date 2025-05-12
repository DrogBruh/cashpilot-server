from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import os

app = Flask(__name__)

@app.route("/credit-offers")
def get_credit_offers():
    try:
        # Настройка Selenium в headless-режиме
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/usr/bin/chromium"  # для Railway/хостинга

        service = Service("/usr/bin/chromedriver")  # фиксированный путь

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.sberbank.com/ru/person/credits/money")

        # Явное ожидание появления карточек
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card__factoids"))
        )

        # Получение всех карточек
        factoids = driver.find_elements(By.CLASS_NAME, "product-card__factoids")

        offers = []
        for block in factoids:
            facts = block.find_elements(By.CLASS_NAME, "factoid")
            sum_text = ""
            term_text = ""

            for fact in facts:
                description = fact.find_element(By.CLASS_NAME, "factoid__description").text.lower()
                value = fact.find_element(By.CLASS_NAME, "dk-sbol-heading").text

                if "срок" in description or "срок кредита" in description:
                    term_text = value
                elif "сумма" in description or "сумма кредита" in description:
                    sum_text = value

            if sum_text and term_text:
                offers.append({
                    "bankName": "Сбербанк",
                    "percent": sum_text,
                    "term": term_text
                })

        driver.quit()
        return jsonify(offers)

    except Exception as e:
        # Возвращаем трассировку ошибки
        error_trace = traceback.format_exc()
        print("=== Ошибка парсинга ===")
        print(error_trace)
        return jsonify({"error": error_trace}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
