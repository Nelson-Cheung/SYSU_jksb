import datetime
import muggle_ocr

sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)


def get_code_text(img_path, bytes):
    with open(img_path, "rb") as f:
        captcha_bytes = f.read()
    text = sdk.predict(image_bytes=captcha_bytes)
    return text


import time
import selenium.common.exceptions
from selenium import webdriver
import requests


def do_jksb(netid, passwd):
    print("*"*30)
    print("{}: start...".format(datetime.datetime.now()))

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    while True:
        driver.get("http://jksb.sysu.edu.cn/infoplus/")

        while True:
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])

            try:
                driver.find_element_by_name("submit")
            except selenium.common.exceptions.NoSuchElementException:
                pass
            else:
                print("jump succeed")
                break

        cookies = driver.get_cookies()[0]
        res = requests.get("https://cas.sysu.edu.cn/cas/captcha.jsp",
                           cookies={cookies['name']: cookies['value']})

        code_path = "sysu_login_code.png"
        with open(code_path, "wb") as f:
            f.write(res.content)
        code_text = sdk.predict(image_bytes=res.content)
        print("code: %s, path: %s" % (code_text, code_path))

        name = driver.find_element_by_id("username")
        name.send_keys(netid)
        name = driver.find_element_by_id("password")
        name.send_keys(passwd)
        name = driver.find_element_by_id("captcha")
        name.send_keys(code_text)
        name = driver.find_element_by_name("submit")

        try:
            name.click()
        except selenium.common.exceptions.WebDriverException:
            print("login succeed")
            break

        try:
            driver.find_element_by_name("submit")
        except selenium.common.exceptions.NoSuchElementException:
            print("login succeed")
            break
        else:
            print("login failed, try again...")

    driver.get("http://jksb.sysu.edu.cn/infoplus/form/XNYQSB/start?membership=Wechat_Enterprise")
    while True:
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])

        try:
            driver.find_element_by_xpath("//a[contains(@id, 'infoplus_action')]")
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            print("jump succeed")
            break

    name = driver.find_element_by_xpath("//a[contains(@id, 'infoplus_action')]")
    time.sleep(1)
    name.click()

    while True:
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])

        try:
            driver.find_element_by_xpath("//a[contains(@id, 'infoplus_action')]")
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            print("submit succeed")
            break

    name = driver.find_element_by_xpath("//a[contains(@id, 'infoplus_action')]")
    time.sleep(1)
    name.click()

    time.sleep(2)
    driver.quit()

    print("{}: done...".format(datetime.datetime.now()))
