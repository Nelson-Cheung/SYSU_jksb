import datetime
import multiprocessing
import threading
import muggle_ocr
import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By

import requests
import os

def wait_by(type, driver, item):
    while True:
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])

        try:

            if type == "xpath":
                driver.find_element(By.XPATH, item)
            elif type == "name":
                driver.find_element(By.NAME, item)
            elif type == "id":
                driver.find_element(By.ID, item)
            elif type == "class name":
                driver.find_element(By.CLASS_NAME, item)

        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            break


def jksb_thread(driver, netid, passwd, success_flag):
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

    print("*"*30)
    print("{}: start...".format(datetime.datetime.now()))

    # code_path = "sysu_login_code"+str(int(time.time() * 100000))+".png"

    while True:
        driver.get("http://jksb.sysu.edu.cn/infoplus/")

        wait_by("name", driver, "submit")
        print("jump to login page succeed")

        cookies = driver.get_cookies()[0]
        res = requests.get("https://cas.sysu.edu.cn/cas/captcha.jsp",
                           cookies={cookies['name']: cookies['value']})

        # with open(code_path, "wb") as f:
        #     f.write(res.content)

        code_text = sdk.predict(image_bytes=res.content)
        # print("code: %s, path: %s" % (code_text, code_path))
        print("code recognization: %s" %(code_text))

        name = driver.find_element(By.ID, "username")
        name.send_keys(netid)
        name = driver.find_element(By.ID, "password")
        name.send_keys(passwd)
        name = driver.find_element(By.ID, "captcha")
        name.send_keys(code_text)
        name = driver.find_element(By.NAME, "submit")

        try:
            name.click()
        except selenium.common.exceptions.WebDriverException:
            print("login succeed")
            break

        try:
            driver.find_element(By.NAME, "submit")
        except selenium.common.exceptions.NoSuchElementException:
            print("login succeed")
            break
        else:
            print("login failed, try again...")

    # os.remove(code_path)

    driver.get(
        "http://jksb.sysu.edu.cn/infoplus/form/XNYQSB/start?membership=Wechat_Enterprise")
    wait_by("xpath", driver, "//a[contains(@id, 'infoplus_action')]")
    print("jump to confirm page succeed")

    name = driver.find_element(By.XPATH, 
        "//a[contains(@id, 'infoplus_action')]")
    time.sleep(1)
    name.click()

    wait_by("class name", driver, "command_button_content")
    print("jump to submit page succeed")

    name = driver.find_element(By.CLASS_NAME, "command_button_content")
    time.sleep(1)
    name.click()

    wait_by("id", driver, "title_description")
    print("jump to finish page succeed")

    number = driver.find_element(By.ID, 
        "title_description").get_attribute('textContent')
    print("submit succeed, {}".format(number))

    print("{}: done...".format(datetime.datetime.now()))

    success_flag.value = True


def jksb_process(netid, passwd, success_flag):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    t = threading.Thread(target=jksb_thread, args=(
        driver, netid, passwd, success_flag))
    t.setDaemon(True)
    t.start()
    t.join(60)

    driver.quit()

    return


def do_jksb(netid, passwd):

    flag = multiprocessing.Value("b", False)

    p = multiprocessing.Process(
        target=jksb_process, args=(netid, passwd, flag))
    p.start()
    p.join()

    return flag.value
