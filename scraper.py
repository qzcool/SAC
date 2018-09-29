from utils import *
from tqdm import *

class Scraper():
    def __init__(self, headless):
        if headless:
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            self.driver = webdriver.Chrome(chrome_options=option)
        else:
            self.driver = webdriver.Chrome()


class Company(Scraper):
    def __init__(self, headless=True):
        self.headless = headless
        super().__init__(headless=self.headless)
        self.url_company_list = 'http://exam.sac.net.cn/pages/registration/sac-publicity-report.html'

    # 获取所有证券公司名单
    def get_company_list(self, save_to_local=True):
        self.driver.get(self.url_company_list)
        time.sleep(8)  # 确保网页完全加载
        content = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(content, 'lxml')

        table = soup.find('div', align='center').find_all('table')[-1]

        # 得到表格标题
        list_columns = []
        for column in table.find_all('tbody')[0].find_all('th'):
            list_columns.append(column.get_text().strip())

        # 得到表格数据
        data, data_aoiId = [], []

        #TODO 考虑是否要定义母类来爬取HTML上的表格
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
        self.driver.quit()
        display(df_companies)

        # 本地保存人员列表
        if save_to_local:
            df_companies.to_csv('列表_证券公司.csv', encoding='gb18030')

        return df_companies

class People(Company):
    def __init__(self, headless=True):
        self.headless = headless
        super().__init__(headless=self.headless)
        # self.url_people_list = 'http://person.sac.net.cn/pages/registration/sac-publicity-finish.html?aoiId='

    # 获取单个公司的所有员工名单
    # TODO: 将company_ID换成公司名称的模糊匹配
    def get_people_list(self, company_ID, display_option=True, sleep_time=1):
        # 启动浏览器
        self.driver.get('http://exam.sac.net.cn/pages/registration/sac-publicity-finish.html?aoiId=' + company_ID)
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
            time.sleep(sleep_time)  # 防止运行过快被封

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
        pages_num = get_pages_num(self.driver)

        # TODO：性能提升-使用deque代替list
        data = []
        data, list_columns = parser(self.driver, data)
        for i in tqdm(range(pages_num - 1)):  ## 最后一页不用点，可以换成while循环更优雅
            change_page(self.driver)
            data, list_columns = parser(self.driver, data)

        self.driver.quit()
        df_people = pd.DataFrame(data, columns=list_columns)

        # 描述表格数据
        print('{}：表格共有{}列，{}行。'.format(df_people.iloc[0,5], len(df_people.columns), len(df_people)))
        if display_option:
            display(df_people)
        return df_people

    # 获取单个员工的照片路径：person_ID即为PPP_ID
    def get_person_info_img(self, person_ID):
        self.driver.get('http://exam.sac.net.cn/pages/registration/sac-finish-person.html?r2SS_IFjjk=' + person_ID)  # '76B6EA9E1C873C0DE053D651A8C06CD1')
        return self.driver.find_elements_by_tag_name('img')[-1].get_attribute("src")

    # 获取单个员工的所有个人信息
    # TODO: 需要挖掘每个人的信息，尽量使用Requests提高速度
    def get_person_info(self, person_ID):
        # 获取单个员工的照片路径
        #url_img = self.get_person_info_img(person_ID)
        # 获取注册变更记录

        pass

    # 批量获取所有公司的所有人的信息
    # TODO：需要使用分布式爬虫来提高速度
    def get_people_list_full(self, save_to_local=True, sleep_time=2):
        # 获取所有公司列表
        df_companies = self.get_company_list(save_to_local=False)

        # 传入所有公司的机构ID，循环爬取
        df_people_full = pd.DataFrame()

        for i in tqdm(df_companies.机构ID):
            df_people = People(headless=self.headless).get_people_list(company_ID=i, display_option=False,sleep_time=sleep_time)
            df_people_full = df_people_full.append(df_people)

        # 描述表格数据
        print('表格共有{}列，{}行。'.format(len(df_people_full.columns), len(df_people_full)))
        display(df_people_full)

        # 本地保存人员列表
        if save_to_local:
            df_people_full.to_csv('列表_从业人员.csv', encoding='gb18030')

        return df_people_full
