# 说在最前面
+ 请合法使用，仅限于用于防守团队内部授权验证，不得用于非法或非授权行为
+ 不提供任何实际攻击代码
+ 基于当前AI发展趋势和作者个人时间问题，本项目不再更新，使用者可遇到错误以采用AI修正，作者正在思考构建利用SKILL技术重新构建类似框架的可行性
# 最新更新
## 2025.01.07
+ 支持导入导出功能
<img width="1716" alt="image" src="https://github.com/user-attachments/assets/4332f226-57cd-4954-84a7-3188e7c9e698" />

+ 支持Nuclei扫描，可以按需配置yaml poc（支持调试），并进行扫描，当前扫描结果验证不稳定，还在优化中，Nuclei使用方法与自定义EXP扫描基本相同
<img width="1473" alt="image" src="https://github.com/user-attachments/assets/ab96a768-bf57-4464-bad4-595732c69055" />
<img width="1476" alt="image" src="https://github.com/user-attachments/assets/63fea92f-4160-4066-a177-b179ea9e52bb" />
<img width="1494" alt="image" src="https://github.com/user-attachments/assets/a60fb669-5ed5-4337-942e-7fc362b8874a" />
<img width="1716" alt="image" src="https://github.com/user-attachments/assets/4332f226-57cd-4954-84a7-3188e7c9e698" />

**使用前请下载nuclei（当前测试版本3.3.7）机器中，并配置路径
<img width="1477" alt="image" src="https://github.com/user-attachments/assets/e6745fbb-2d27-4d4e-af77-0bf98be2756b" />

+ 新增员工和排班功能
<img width="1728" alt="image" src="https://github.com/user-attachments/assets/11d27de7-52de-46ef-8faf-998a72d3d597" />
<img width="1702" alt="image" src="https://github.com/user-attachments/assets/2c578e75-3b0e-4d8d-b348-3b46f8bd067d" />


  
## 2023.09.14 
+ 增加新功能，可以支持根据关键字监控Github上面新的漏洞POC/EXP
<img width="1434" alt="image" src="https://github.com/b0bac/ApolloScanner/assets/11972644/b815ec72-6aeb-44e2-ac2b-e2b31d7f54c4">

![image](https://github.com/b0bac/ApolloScanner/assets/11972644/315f8ef1-5649-483c-b40e-d0b31dd987e7)



```bash
python3 manage.py crontab add # 添加计划任务
python3 manage.py crontab show # 查看计划任务
```


## 2023.09.12 
+ 优化显示逻辑
## 2023.09.11
+ 更新了依赖库和安装说明文件
+ 修复了virustotal请求验证证书失败的问题
+ 修复github找不到Github的问题
+ 修复了详情扫描中间件具体信息不能扫描的问题的


# 通知

**请因缺少依赖库、依赖库版本不对、缺少组件、数据库账号口令与配置文件不同等引发的报错的使用者，先自行Google解决。**

**对于没有兴趣自己解决环境报错的小伙伴们，这里提供了虚拟机文件可直接下载导入运行。**
# ApolloScanner
自动化巡航扫描框架（可用于红队打点评估）
![图片](https://user-images.githubusercontent.com/11972644/158723361-8356e64d-55fa-40df-a39c-2b52561726ab.png)


## 安装
**版本更新，不再支持虚机安装,请使用源码安装，部署过程的Trouble Shooting 也是一种成长**
+ python版本： 3.8.x 或 3.9.x
+ django版本：4.0.1
+ nmap：需要
+ masscan：需要
+ nuclei：若要使用则需要，请自行下载
+ mysql
+ 前端：基于simple-ui
+ 支持操作系统：Ubuntu 20.04
+ 应该支持但未测试：MacOS 系列/ Ubuntu 系列

```python
sudo apt install masscan nmap libmysqlclient-dev mysql-server
sudo python3 -m pip install -r requirments.txt
# 需要手动修改mysql root密码 创建Apollo 数据库 并修改settings.py 中的数据库账密
sudo python3 manage.py migrate
sudo python3 manage.py createsuperuser
sudo python3 manage.py runserver 0.0.0.0:80
```

## 功能
+ 资产收集（需要主域名，资产对象可直接在爆破和漏扫过程中调用）
  + 子域名收集（需要virustotal-api-token）
  + cname收集
  + ip地址（a记录）收集
  + 开放端口扫描（基于masscan）
  + 端口对应服务、组件指纹版本探测（基于nmap）
  + http标题探测
  + http框架组件探测

+ github敏感信息收集
  + 基于域名和关键字的敏感信息收集（需要github-token）
  + 
+ 暴力破解（基于exp的暴力破解）
  + exp注册模块
    + 代码动态编辑
    + 代码动态调试
    + 支持资产对象
  + 破解任务模块
    + 支持exp对象调用
    + 支持资产对象
    + 支持批量资产 
    + 支持多线程（可配置） 
  + 破解结果模块
    + 支持结果显示
    + 支持钉钉通知
  + 敏感路径探测任务
  + 敏感路径探测结果  
  
+ 漏洞扫描模块
  + exp注册模块 
    + 代码动态编辑
    + 代码动态调试
    + 支持资产对象
  + 漏扫任务模块
    + 支持exp对象调用
    + 支持资产对象
    + 支持批量资产 
    + 支持多线程（可配置) 
  + 结果显示模块
    + 支持结果显示
    + 支持钉钉通知
   
+ 配置模块
  + 支持常用系统配置（各类token、线程数）
  + 支持用户、用户组、权限配置模块
  + 支持启动服务模块
    + HTTP服务（支持HTTP请求记录）
    + DNS服务（支持DNS请求记录） 

## exp编写规范
+ 暴力破解
```python
def brute_scan_function_name(ipaddress, port, username, password, logger):  
    import xx_module # 引入模块全部在函数内容写
    # ... 
    # ...是爆破exp核心代码
    logger.log("xxxxx") # 代替print
    return True  # 返回必须是true/false
```
+ 漏扫扫描
```python
def brute_scan_function_name(ipaddress, port, logger):  
    import xx_module # 引入模块全部在函数内容写
    # ... 
    # ...是漏扫exp核心代码
    logger.log("xxxxx") # 代替print
    return True  # 返回必须是true/false
```

## 报错解答
### 1、缺乏mysql_config命令：
+ 报错示例
```
Preparing metadata (setup.py) ... error
error: subprocess-exited-with-error

× python setup.py egg_info did not run successfully.
│ exit code: 1
╰─> [11 lines of output]
/bin/sh: 1: mysql_config: not found
Traceback (most recent call last):
File "", line 2, in
File "", line 34, in
File "/tmp/pip-install-2er683ou/mysqlclient_5ba8560cf6ca429b8316cf1cf6771c9a/setup.py", line 16, in
metadata, options = get_config()
File "/tmp/pip-install-2er683ou/mysqlclient_5ba8560cf6ca429b8316cf1cf6771c9a/setup_posix.py", line 51, in get_config
libs = mysql_config("libs")
File "/tmp/pip-install-2er683ou/mysqlclient_5ba8560cf6ca429b8316cf1cf6771c9a/setup_posix.py", line 29, in mysql_config
raise EnvironmentError("%s not found" % (_mysql_config_path,))
OSError: mysql_config not found
[end of output]

note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.
```
+ 解析：由于部分环境缺乏mysql_config命令导致mysqlclient依赖安装失败，可能是由于没有安装该命令或者没有建立该命令的软连接，可根据自己环境google解决。
+ 参考文献 : [解决Mysql中mysql_config not found的方法](https://www.cnblogs.com/alice-bj/articles/9512426.html)

### 关于一些异常简单的报错的解答：
**目前看到一些ISSUE报错的原因是以下几种情况：**
+ 自己环境mysql账号密码与配置文件不匹配
+ 缺少相关依赖Python库或版本不对
+ 缺少相关依赖的组件或版本不对
**此类问题请自行Google解决，不要提ISSUE**
