# 源码目录结构
## WorkHourSystem
工时管理系统包含用户模块、项目管理员模块、系统管理员模块等（当前系统管理员账号：superadmin，密码：123123）。如需初始化系统,请删除WorkHourSystem下的WHMGSystem.db，重启服务器即可设置系统管理员账号，具体说明如下。

### 1、views
系统路由相关包，位于系统控制层，包含如下文件：
> user.py：  
普通用户页面的路由包，主要包括系统用户信息的获取以及用户相关的数据操作。

> admin.py  
项目管理员页面路由包，项目管理员路由均添加于此脚本文件中。

> super_admin.py  
系统管理员页面路由包，系统管理员路由均添加于此脚本文件中。

> api.py  
系统公共api路由包，系统公共api路由均添加于此脚本文件中。

### 2、service
用于控制层调用的服务代码，位于系统逻辑处理层：

#### 1、handle
用于用户操作逻辑代码包，包含如下文件：

> companyService.py
实现公司相关数据修改操作独立功能模块。

> departmentService.py  
实现部门相关数据修改操作独立功能模块。

> jindeeService.py  
实现金蝶服务相关数据修改操作独立功能模块。

> projectService.py  
实现公司项目相关数据修改操作独立功能模块。

> userService.py  
实现系统用户相关数据修改操作独立功能模块。

> workhourService.py  
实现用户工时相关数据修改操作独立功能模块。

#### 2、view
负责所有用户页面数据生成，包含如下文件：

> adminViewService.py  
负责生成项目管理员各页面数据。

> superAdminViewService.py  
负责生成系统管理员各页面数据。

> userViewService.py  
负责生成普通用户各页面数据。

### 3、model
系统数据持久化模型层，提供服务层调用对数据库进行操作，系统模型层，包含如下文件：

> company.py  department.py user.py等文件

### 4、templates
 系统前端模板,视图层
 

### 5、static
系统前端模板中所使用的所有脚本，样式和字体文件。
 
### 6、decorators
系统路由自定义装饰器包，用于检测拦截用户权限

> authorize_required.py  
包含普通用户、项目管理员、系统管理员、api、权限装饰器


### 7、utils
系统工具包，包含如下文件：

> DbPoolUtil.py  
实现DBUtils数据库框架，用于链接金蝶数据库连接池。

> DBUtils.py  
用于检测数据库是否初始化，和初始化功能，包含数据库所有结构sql语句。

> excelUtils.py
实现生成excel表格工具类

> MD5utils.py
实现md5工具，主要有用于对密码进行不可逆加密

> strUtils.py
字符串工具类

>timeUtils.py
时间工具类，主要用于工时查询

### 8、syslog
系统日志相关的操作，包含如下文件：
> systemlog.py  
系统日志模块，用于定义系统运行日志的文件、输出结构，日志级别等参数信息。

### 9、conf
系统部分全局变量以及运行参数配置的包，包含如下文件：
> initsystem.py  
系统服务启动的初始化程序，主要用于系统服务开启时所进行的准备工作，开发中相关的函数与配置均添加于该脚本文件中。

> setting.py  
系统相关的全局变量和常量配置文件，开发中定义系统配置参数与常量均在此脚本文件中进行。


### 10、jinja2_fun
用于存放jinja2模板提供的函数，包含如下文件：
> workHour.py  
工时数据格式化等函数


## requirements.txt
搭建系统运行环境所需要的Python软件包及其版本号。

## runserver
系统服务启动程序脚本。
