# 中国证券业协会相关数据分析 Data Analysis for SAC
Data Analysis Bundles for Securities Association of China (SAC).

## 数据获取及开源 Data Acquisition and Open-source
提供经过整理的证券业协会公开数据，格式为CSV/JSON，定期自动更新。
Open-source structured public data of SAC, in .csv/.json format, regularly auto-updated.
1. 证券公司
全列表
2. 从业人员
全列表，所有公司信息合并


## [从业人员执业注册信息公示 SAC Publicity Report](http://person.sac.net.cn/pages/registration/sac-publicity-report.html)
1. 证券公司分析 Securities Corporations Analysis
    1. 共121家证券公司，一般证券业务比例
1. 从业人员跳槽及流向分析
2. 学历分析
    1. 博士生比例
3. 历年招聘情况分析：根据每月新增注册证书数量来统计
4. 男女比例分析
5. 证券公司人数频数分布图
6. 近视比率：使用腾讯人脸识别API
7. 从业类型分类
8. 颜值相关
    1. 高分妹发掘器：占公司的比率
    2. 公司平均颜值
    3. 平均颜值变化情况：随入职年限

## 技术栈 Tech Stack
### 数据开源 Data Acquisition
1. Python 3.6, 
2. **Selenium/Scrapy?**
3. 尝试使用分布式爬虫加快速度

### 数据可视化 Data Visualization
2. Python, d3.js/E-Charts
1. SmartBI

## 反馈 Feedback
欢迎提出在issues中提出你感兴趣的问题。 Feel free to send a pull request or report an issue. Also, welcome to drop your questions about SAC and we will see if new features should be integrated.  
