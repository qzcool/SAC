from tqdm import *
from selenium import webdriver


class Scraper():
    def __init__(self, headless):
        if headless:
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            self.driver = webdriver.Chrome(chrome_options=option)
        else:
            self.driver = webdriver.Chrome()


if __name__ == "__main__":
    Scraper()