import requests
from pyquery import PyQuery
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time
import re

class Scraper(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self,login,pass_):
        self.driver.get("https://csgopolygon.gg/?login")

        username = WebDriverWait(self.driver, 200).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='username']")))
        password = WebDriverWait(self.driver, 200).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='password']")))
        login_button = WebDriverWait(self.driver, 200).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='login_btn_signin']/input")))

        username.click()
        username.send_keys(login)

        password.click()
        password.send_keys(pass_)

        login_button.click()

        code = input("Steam code: ")

        if self.steam_code(code):
            return True
        return False

    def steam_code(self,code):
        try:
            code_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@id='twofactorcode_entry']")))
            code_input.click()
            code_input.send_keys(code)

            login_buttons = self.driver.find_elements_by_class_name("auth_button")
            login_buttons[10].click()

            try:
                accept =  WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@onclick='acceptAgreement();']")))
                accept.click()

                time.sleep(2)

                navbar = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@data-target='#navbar']")))
                navbar.click()
            except:
                pass

            roll_status = self.driver.find_element_by_xpath("//div[@id='past']")

            if roll_status:
                return True
            return False
        except:
            return False

    def get_values(self):
        roll_status = self.driver.find_element_by_xpath("//span[@id='banner']")

        if roll_status.text == "***ROLLING***":
            while roll_status.text == "***ROLLING***":
                time.sleep(0.2)

            if "Rolled" in roll_status.text:
                past_balls = []

                rolled = re.sub("[^0-9]", "", roll_status.text)

                balls = self.driver.find_elements_by_xpath("//div[@id='past']/div")

                for ball in balls:
                    past_balls.append(int(ball.text))

                return [rolled, past_balls]

        return False

    def close_modal(self):
        try:
            accept = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@onclick='acceptAgreement();']")))
            accept.click()
        except:
            pass

    def get_rolls(self):
        output = []

        r = requests.get("https://csgopolygon.gg/rolls.php")
        html = PyQuery(r.text)

        for tr in html.find("tr").items():
            seed = tr("td").eq(1)
            lottery = tr("td").eq(2)
            rolls = tr("td").eq(3)


            if seed.text() != "SERVER SEED IN USE" and len(seed.text()) > 1:
                rolls =  str(rolls.text())
                rolls = rolls.split("-")
                roll_start = rolls[0]
                roll_finish = rolls[1]

                output.append({"hash" : seed.text(),"lottery" : lottery.text(),"roll_start" : roll_start,"roll_finish" : roll_finish})
        return output

    def make_bet(self,amount,color):
        try:
            input_amount = self.driver.find_element_by_id("betAmount")
            input_amount.click()
            input_amount.send_keys(Keys.CONTROL + "a")
            input_amount.send_keys(Keys.DELETE)
            input_amount.send_keys(int(amount))

            bet_blocks = self.driver.find_elements_by_class_name("betBlock")
            time.sleep(3)

            if color == 0:
                self.driver.execute_script('$(".betButton")[1].click();')
            elif color == 1:
                self.driver.execute_script('$(".betButton")[0].click();')
            elif color == 2:
                self.driver.execute_script('$(".betButton")[2].click();')

            return True
        except Exception as e:
            print(str(e))
            return False
