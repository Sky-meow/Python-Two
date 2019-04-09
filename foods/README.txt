食堂/项目 预定点餐系统
./apps/ 为Application所在路径
./django_extra 为扩展包所在路径
./foods 为主目录以及系统配置
./static 为静态文件路径
./requirements.txt 为需要的第三方扩展包
./customer/api.py 有三个类型的api写法例子

pip install -r requirements.txt 通过文档安装扩展包

如何本地运行:
在不修改数据库配置的情况下:
1.进入项目根目录
2.使用python manager.py createsuperuser 创建超级管理员用户
3.使用 python manager.py runserver 运行服务
4.进入浏览器,输入 localhost:8000 或者 其他配置好的域名 进行访问
    4.1 后台路径是 /admin/
    4.2 前端路径则是直接域名
    4.3 api文档地址默认情况下是 /api/docs/
    注意: 如果路由有变动,则根据自己定义的路由进行访问

注意事项:
1.创建的应用全部归入apps/目录
2.创建api的话,需要在对应的app目录下创建 api文件夹,包含 "方法文件".py 与url[s].py 两个文件
    2.1. "方法文件".py 用于写对应的API(接口)方法
    2.2. urls.py或者url.py 用于编写对应api的路由
    2.3 app的普通视图方法,则写入对应的views.py,路由写入到app根目录下的urls.py或者url.py下
3.自定义的api,只需使用 from api import * 则可以引入常用的编写api所需要的类
4.使用from api.permission import checkToken 则可以引入检测是否登陆和是否合法的装饰器 checkToken
[3,4的引入内容可以自行查看api.__init__]


2019-04-08: 添加store相关包的功能和api
