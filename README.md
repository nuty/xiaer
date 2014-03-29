xiaer
=====

虾米音乐试听记录数据爬取和可视化。

通过输入虾米网用户ID,爬取用户的试听记录保存到数据库中，通过js画出饼图，前端在页面展示。


##有坑!!

#### 未解决的问题
    1,没有做用户模拟登录
    2,当爬虫运行时没有提示，抓取完成后会弹出对话框
    ....


#### 使用的工具
    flask web框架
    highcharts javaScript图表库
    requests  网络请求
    pyquery  解析html文本

#### 运行
    创建虚拟环境
    mkvirtualenv xiaer
    
    安装依赖
    pip install -r requirements.txt
    
    初始化数据库
    python manage.py initdb

    运行服务
    python manage.py runserver

