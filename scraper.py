import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests, time, re, math, openpyxl, datetime, os, shutil, psutil, platform, pyautogui, subprocess, webbrowser, json, codecs, pyperclip
from tqdm import *
import xlwings as xw
from selenium import webdriver
from IPython.display import display, HTML
from collections import OrderedDict

class Company():
    def __init__(self):
        self.url_company_list = 'http://person.sac.net.cn/pages/registration/sac-publicity-report.html'

    # 获取所有证券公司名单
    def get_company_list(self):
        driver = webdriver.Chrome()
        driver.get(self.url_company_list)
        time.sleep(8)  # 确保网页完全加载
        content = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(content, 'lxml')

        table = soup.find('div', align='center').find_all('table')[-1]

        # 得到表格标题
        list_columns = []
        for column in table.find_all('tbody')[0].find_all('th'):
            list_columns.append(column.get_text().strip())

        # 得到表格数据
        data, data_aoiId = [], []

        #TODO 考虑是否要定义母类
        for row in table.find_all('tbody')[1].find_all('tr'):
            cols = row.find_all('td')
            data_aoiId.append(cols[1].find('a')['onclick'].split('(')[1].split(')')[0])  # 得到机构ID
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # Get rid of empty values

        df_companies = pd.DataFrame(data, columns=list_columns)
        df_companies_id = pd.DataFrame(data_aoiId, columns=['机构ID'])  # 插入机构ID
        df_companies = pd.concat([df_companies, df_companies_id], axis=1)

        # 描述表格数据
        print('表格共有{}列，{}行。'.format(len(df_companies.columns), len(df_companies)))
        driver.quit()
        display(df_companies)

        return df_companies

# TODO: 是否要设置People和Company类别的继承关系：考虑可能
class People(Company):
    def __init__(self):
        pass
        # super.
        # self.url_people_list = 'http://person.sac.net.cn/pages/registration/sac-publicity-finish.html?aoiId='