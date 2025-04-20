import streamlit as st
st.write("start")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

st.write("libraries imported")

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
CHROME_BINARY_PATH = "/usr/bin/chromium"

options = Options()
options.binary_location = CHROME_BINARY_PATH
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

st.write("options set")

st.title("jRCT検索アプリ")
st.write("疾患名とフリーワードを入力してください。")

disease_name = st.text_input("疾患名", "肺がん")
free_keyword = st.text_input("フリーワード", "EGFR")
search_button = st.button("検索開始")

if search_button:
    st.write("検索開始ボタンクリック検知")

    try:
        driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
        st.write("WebDriver 初期化成功")

        driver.get("https://jrct.mhlw.go.jp/search")
        st.write("ページ遷移成功")

        # 以下も必要に応じて st.write() を挿入可能
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "reg-plobrem-1"))).send_keys(disease_name)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "demo-1"))).send_keys(free_keyword)

        checkbox = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "reg-recruitment-2")))
        if not checkbox.is_selected():
            checkbox.click()

        st.write("検索条件入力完了")

        search_button_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "検索")]'))
        )
        driver.execute
