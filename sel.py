import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
import sys

def get_exchange_rate(date, currency_code):

    # 创建WebDriver对象
    driver = webdriver.Chrome()

    try:
        # 打开目标网页
        driver.get('https://www.boc.cn/sourcedb/whpj/')  # 替换为目标网页地址

        start_date_input = driver.find_element(By.NAME, 'erectDate')  # 替换为实际起始时间输入框的名称或ID

        # 使用JavaScript调用日期选择器
        driver.execute_script("arguments[0].click();", start_date_input)
        time.sleep(1)  # 等待1秒钟以确保日期选择器加载完成

        # 点击日期选择器后，您可以继续模拟操作，例如选择日期
        # 例如，选择2022年12月1日
        selected_date = '2022-12-01'
        driver.execute_script(f"document.getElementsByName('erectDate')[0].value='{selected_date}';")

        end_date_input = driver.find_element(By.NAME, 'nothing')  # 替换为实际起始时间输入框的名称或ID

        # 使用JavaScript调用日期选择器
        driver.execute_script("arguments[0].click();", end_date_input)
        time.sleep(1)  
        selected_date = '2022-12-01'
        driver.execute_script(f"document.getElementsByName('nothing')[0].value='{selected_date}';")
        
        
        options = driver.execute_script("return Array.from(document.querySelectorAll('#pjname option')).map(option => option.value)")

        


            # 等待货币选择框可见
        currency_select_box = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.ID, 'pjname')))

        # 点击货币选择框以展开选项
        driver.execute_script("arguments[0].click();", currency_select_box)

        # 等待货币选项可见
        currency_option = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "//option[@value='英镑']")))

        # 选择货币
        currency_option.click()

            # 在货币代号输入框中输入货币代号
        currency_input = driver.find_element(By.NAME, 'currency_code')  # 替换为实际货币代号输入框的名称或ID
        currency_input.clear()
        currency_input.send_keys(currency_code)

        # 提交表单
        currency_input.send_keys(Keys.RETURN)

        # 等待页面加载完成
        driver.implicitly_wait(10)

        # 获取现汇卖出价
        exchange_rate_element = driver.find_element(By.XPATH, '//table//tr[td[contains(text(), "' + currency_code + '")]]/td[4]')
        exchange_rate = exchange_rate_element.text

        return exchange_rate

    finally:
        # 关闭WebDriver和服务
        driver.quit()
        # service.stop()

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python3 yourcode.py <date> <currency_code>")
    #     sys.exit(1)

    date = '20220101'
    currency_code = 'USD'

    exchange_rate = get_exchange_rate(date, currency_code)
    if exchange_rate:
        print(exchange_rate)
    else:
        print("Exchange rate not found for the given date and currency code.")
