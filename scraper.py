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

    # 获取单个公司的所有员工名单
    def get_people_list(self, company_ID):
        # 启动浏览器
        # TODO：添加Headless选项
        driver = webdriver.Chrome()
        driver.get('http://person.sac.net.cn/pages/registration/sac-publicity-finish.html?aoiId=' + company_ID)
        time.sleep(2)  # Driver加载完如果直接取数最好设置延迟

        # 确认页数
        def get_pages_num(driver):
            pages_num = 0  # 保证即便确认页数错误，仍然可以获得第一页而不会终止程序
            try:
                pages_num = int(float(driver.find_element_by_id('sp_1').text.strip()))
            except Exception as e:
                print('请修改确认页数的ID标签，错误代码为：', e)
            finally:
                return pages_num

        # 翻页
        def change_page(driver):
            driver.find_element_by_id('next_t').click()
            time.sleep(2)  # 防止运行过快被封

        # 爬取单页
        def parser(driver, data):
            content = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(content, 'lxml')
            table = soup.find('div', class_='listable_out').find('table', class_='ui-jqgrid-htable')

            # 得到表格标题
            list_columns = []
            for column in table.find_all('tr')[0].find_all('th'):
                list_columns.append(column.get_text().strip())

            # 得到表格数据
            for row in soup.find('div', class_='ui-jqgrid-bdiv').find_all('tr', id=True):
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])  # Get rid of empty values

            return data, list_columns

        # 主程序部分
        pages_num = get_pages_num(driver)

        data = []
        data, list_columns = parser(driver, data)
        for i in tqdm(range(pages_num - 1)):  ## 最后一页不用点，可以换成while循环更优雅
            change_page(driver)
            data, list_columns = parser(driver, data)

        driver.quit()
        df_people = pd.DataFrame(data, columns=list_columns)

        # 描述表格数据
        print('表格共有{}列，{}行。'.format(len(df_people.columns), len(df_people)))
        display(df_people)
        return df_people

    # 获取单个员工的所有个人信息
    def get_people_info(self, person_ID):
        pass

    # 批量获取所有公司的所有人的信息
    # TODO：需要使用分布式爬虫来提高速度