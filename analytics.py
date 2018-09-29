from utils import *

# 暴露出数据接口，方便以后生成Dashboard


# 超类
class Analytics():
    def __init__(self):
        self.df_people_full = pd.read_csv('列表_从业人员.csv', encoding='gb18030')


# 基础分析类：https://github.com/qzcool/SAC/milestone/1
class Basic(Analytics):
    def __init__(self):
        super().__init__()

    # 性别比率：保存为JSON，支持公司级别和总计
    def basic_gender(self):
        # 总计
        df_total = self.df_people_full.groupby(by=['性别']).size().to_frame('人数')
        # 按公司
        df_company = self.df_people_full.groupby(by=['执业机构', '性别']).size().to_frame('人数')
        # 按学历
        df_degree = self.df_people_full.groupby(by=['学历', '性别']).size().to_frame('人数')
        # 按执业岗位
        df_role = self.df_people_full.groupby(by=['执业岗位', '性别']).size().to_frame('人数')
        # 按注册变更记录：男性跳槽更多
        df_alter_record = self.df_people_full.groupby(by=['注册变更记录', '性别']).size().to_frame('人数')
        # TODO：按证书取得日期，做随年份的河流图

        dic_gender = OrderedDict([('总计', df_total), ('按公司', df_company), ('按学历', df_degree), ('按执业岗位', df_role), ('按注册变更记录', df_alter_record)])
        return Writer_JSON().odict_to_json(dic_gender)


# 高级分析类：https://github.com/qzcool/SAC/milestone/4
class Advanced(Analytics):
    def __init__(self):
        super().__init__()