# 中国证券业协会数据分析和可视化 Data Analysis and Visualization for SAC
Data Analysis and Visualization for Securities Association of China (SAC).

## 数据获取及开源 Open Data 
提供**经过整理的证券业协会公开数据和其他开源渠道数据**，格式为CSV，定期自动更新。
Open-source structured public data of SAC, in .csv format, regularly auto-updated.
1. 证券公司：全列表,大约8KB。
2. 从业人员：全列表，所有公司信息合并显示，大约30MB。

## [从业人员执业注册信息公示 SAC Publicity Report](http://person.sac.net.cn/pages/registration/sac-publicity-report.html)
所有数据分析都会函数化并输出为JSON文件API，以便后续可视化等应用的调用。

## 安装和使用
请根据`requirements.txt`文件的声明安装所有依赖。`start.ipynb`文件包含所有函数的调用方法实例。

## 技术栈 Tech Stack
| 模块 Module            | 使用的依赖 Dependencies                                  |
|-------------------------------|-------------------------------------------------|
| 数据开源 Open Data            | Selenium                                         |
| 数据分析 Data Analysis        | pandas                                           |
| 数据可视化 Data Visualization | Plotly/Dashboard, D3.JS/ECharts.JS, GitHub Pages |

## 反馈 Feedback
欢迎提出在issues中提出你感兴趣的问题。 Feel free to send a pull request or report an issue. Also, welcome to drop your questions about SAC and we will see if new features should be integrated.  
