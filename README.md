# ApolloScanner
自动化巡航扫描框架（可用于红队打点评估）
![图片](https://user-images.githubusercontent.com/11972644/158723361-8356e64d-55fa-40df-a39c-2b52561726ab.png)


## 安装
+ python版本： 3.8.x 或 3.9.x
+ django版本：4.0.1
+ nmap：需要
+ masscan：需要
+ mysql
+ 前端：基于simple-ui

```python
sudo python3 -m pip install -r requirments.txt
sudo python3 manage.py migrate
sudo python3 manage.py createsuperuser
sudo python3 manage.py runserver
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

+ 敏感路径探测
  + 探测任务
  + 探测结果  
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
