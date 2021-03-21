## fisher 鱼书

Python公益赠书网站 

1. [项目介绍](#一项目介绍)
2. [开发环境](#二开发环境)
3. [使用方法](#三使用方法)
4. [项目结构](#四项目结构)
5. [开发计划](#五开发计划)
6. [结语](#六结语)

---

#### 一、项目介绍

fisher是一个开源并免费的图书捐赠网站项目，核心思想：给旧书拥有者，图书索取者提供一个平台去进行图书交换，实现图书利用的良性循环。该项目采用Python3+Flask+Mysql+Git技术，以flask轻量型web应用框架为基础，集成多个第三方扩展库：flask-sqlalchemy库实现ORM的对象关系映射，简化了对数据直接操纵，以及数据库的跨平台等问题；flask-mail库实现电子邮箱的异步发送，flask-login库实现用户的登录管理。通过访问第三方的图书信息接口，将数据存储在mysql数据库中。Git实现项目的版本控制，对项目的后续优化，版本发布，同时在 [码云](https://gitee.com/weeinn/fisher) 和 [github](https://github.com/weeinn/fisher) 上开源。

#### 二、开发环境

以下是该项目使用的环境

* Python：3.7.9
* Pipenv：version 2020.11.15
* 开发IDE：PyCharm 专业版 2020.3.2
* 系统：Windows 10
* 数据库：MySQL 5.7

#### 三、使用方法

1. 首先准备上述环境

2. 点击克隆clone/下载download，可以直接点下载ZIP，本地解压完成后，直接在PyCharm中打开。

3. 由于安全性，隐私等问题还有一个配置文件secure.py没有提交，里面是数据库以及电子邮箱的参数配置。

   ![secure](https://images2.imgbox.com/57/29/PpSgwevg_o.png "配置文件")

4. 可以在config文件下面新建该文件，然后运行项目，根据报错或警告信息，来配置参数，电子邮箱功能如果不使用，只需要配置数据的URL信息。

5. 右键run，运行成功

#### 四、项目结构

```
fisher
	-app
        -api  接口蓝图
        -cms  内容管理蓝图
        -config 配置文件
        -forms 验证层
        -libs  自定义工具类
        -models 模型层
        -spider  持久层
        -view_models 数据处理
        -web  路由 控制层
        -static 静态文件
        -template 模板
        -__init__.py 初始化
        -test 测试文件(未提交)
   -.gitignore 忽略文件
   -Pipfile 配置包依赖
   -Pipfile.lock 锁包版本
   -README.md 说明文档
   -fisher.py 入口文件
```

#### 五、开发计划

本次开发采用的是前后端不分离进行开发的，期间存在一定程度的耦合。

制定的后期开发计划：

​		1.采用vue框架优化前端  

​		2.采用django重构后台 

​		3.使用mongodb+redis对数据性能优化

​		4.整合相关模块

​		5.部署到服务器

#### 六、结语

欢迎任何形式的贡献，包括发现问题，发送代码块，或创建拉请求。由于个人水平有限，项目难免存在不妥之处，如若发现，恳请及时指正，联系方式📫：weeinnstudio@qq.com。[回到顶部](#fisher-鱼书)

