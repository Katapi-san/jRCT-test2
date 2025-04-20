import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ServiceにChromedriverのパスを明示的に指定
service = Service("/usr/lib/chromium-browser/chromedriver")  # Streamlit Cloudではこちらのパスが正解

# UI
st.title("jRCT検索アプリ")
st.write("疾患名とフリーワードを入力してください。")

disease_name = st.text_input("疾患名", "肺がん")
free_keyword = st.text_input("フリーワード", "EGFR")
search_button = st.button("検索開始")

if search_button:
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    try:
        driver = webdriver.Chrome(service=service, options=options)
        st.success("WebDriver initialized successfully!")

        # jRCT検索ページ処理
        driver.get("https://jrct.mhlw.go.jp/search")
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "reg-plobrem-1"))
        )
        search_box.send_keys(disease_name)

        keyword_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "demo-1"))
        )
        keyword_box.send_keys(free_keyword)

        recruitment_checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "reg-recruitment-2"))
        )
        if not recruitment_checkbox.is_selected():
            recruitment_checkbox.click()

        search_button_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "検索")]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button_element)
        time.sleep(1)
        search_button_element.click()

        rows = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.table-search tbody tr"))
        )
        results = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            results.append({
                "臨床研究実施計画番号": cols[0].text.strip(),
                "研究の名称": cols[1].text.strip(),
                "対象疾患名": cols[2].text.strip(),
                "研究の進捗状況": cols[3].text.strip(),
                "公表日": cols[4].text.strip(),
                "詳細": cols[5].find_element(By.TAG_NAME, "a").get_attribute("href")
            })

        st.write("検索結果:")
        for result in results:
            st.write(result)

    except Exception as e:
        st.error(f"Error initializing WebDriver: {str(e)}")

    finally:
        if 'driver' in locals():
            driver.quit()
