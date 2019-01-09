from modules.utils import *

# 暴露出数据接口，且只输出原始数据而不包含计算字段，方便以后生成Dashboard


# 超类
class Analytics():
    def __init__(self):
        self.df_people_full = pd.read_csv('列表_从业人员.csv', encoding='gb18030', engine='python')
        # 参考: https://stackoverflow.com/questions/50552404/oserror-initializing-from-file-failed-on-csv-in-pandas


# 基础分析类：https://github.com/qzcool/SAC/milestone/1
class Basic(Analytics):
    def __init__(self):
        super().__init__()

    # 性别比率：保存为JSON，支持公司级别和总计
    def basic_gender(self):
        # 总计
        df_total = self.df_people_full.groupby(by=['性别']).size().to_frame('人数').sort_values(by='人数', ascending=False)
        # 按公司
        df_company = self.df_people_full.groupby(by=['执业机构', '性别']).size().to_frame('人数')
        # 按学历
        df_degree = self.df_people_full.groupby(by=['学历', '性别']).size().to_frame('人数')
        # 按执业岗位
        df_role = self.df_people_full.groupby(by=['执业岗位', '性别']).size().to_frame('人数')
        # 按注册变更记录：男性跳槽更多
        df_alter_record = self.df_people_full.groupby(by=['注册变更记录', '性别']).size().to_frame('人数')
        # TODO：按证书取得日期，做随年份的河流图

        # TODO:此处如何实现代码复用？即将生成字典的过程根据变量个数不同自动函数化？
        dic_gender = OrderedDict([('总计', df_total), ('按公司', df_company), ('按学历', df_degree), ('按执业岗位', df_role), ('按注册变更记录', df_alter_record)])
        return Writer_JSON().odict_to_json(dic_gender)

    # 行业新增人数
    def basic_date_registration(self):
        # 按日：基础
        df_date_registration = self.df_people_full.groupby(pd.Grouper(key='证书取得日期')).size().to_frame('人数').sort_values(by='证书取得日期')
        # 按月：基于基础

        # 按年：基于基础

        dic_data_registration = OrderedDict([('按日', df_date_registration)])
        return Writer_JSON().odict_to_json(dic_data_registration)

    # 执业类型分类
    def basic_role(self):
        # 总计
        df_total = self.df_people_full.groupby(by=['执业岗位']).size().to_frame('人数').sort_values(by='人数', ascending=False)
        # 按性别

        # 按证书取得日期

        # 按学历

        dic_role = OrderedDict([('总计',df_total)])
        return Writer_JSON().odict_to_json(dic_role)

    # 学历分析
    def basic_degree(self):
        # 总计
        df_total = self.df_people_full.groupby(by=['学历']).size().to_frame('人数').sort_values(by='人数', ascending=False)
        # 按证券公司：观察不同公司不同学历人群的所占比例
        df_company = self.df_people_full.groupby(by=['执业机构','学历']).size().to_frame('人数')
        # 博士研究生所在证券公司分布
        df_degree_phd = self.df_people_full[self.df_people_full['学历']=='博士研究生'].groupby(by=['执业机构']).size().to_frame('人数').sort_values(by='人数', ascending=False)
        # 硕士研究生所在证券公司分布
        df_degree_master = self.df_people_full[self.df_people_full['学历']=='硕士研究生'].groupby(by=['执业机构']).size().to_frame('人数').sort_values(by='人数', ascending=False)

        dic_degree = OrderedDict([('总计', df_total), ('按证券公司', df_company), ('博士研究生所在证券公司分布', df_degree_phd), ('硕士研究生所在证券公司分布', df_degree_master)])
        return Writer_JSON().odict_to_json(dic_degree)

    # 证券公司分析
    def basic_company(self):
        # 总计
        df_total = self.df_people_full.groupby(by=['执业机构']).size().to_frame('人数').sort_values(by='人数', ascending=False)

        dic_company = OrderedDict([('总计', df_total)])
        return Writer_JSON().odict_to_json(dic_company)

# 高级分析类：https://github.com/qzcool/SAC/milestone/4
class Advanced(Analytics):
    def __init__(self):
        super().__init__()