1. 了解你有没有自动化测试项目的实战经验
    - 有没有做过自动化测试
    - 请举例说明下，你在编写自动化脚本过程中碰到了哪些异常
        - NoSuchElementException、TimeoutException、NoSuchFrameException
    - 是如何在公司里面实施自动化测试
2. 你在自动化领域里面的技术深度怎么样



# postman接口关联 接口依赖
## 全局变量获取方法 {{}}
1. JSON提取器 (都是从返回数据中提取)
    - 在Tests中写JavaScript 将需要提取的值设置成postman中的global变量 
    - `console.log(responseBody);var jsonData = JSON.parse(responseBody)`
    - `pm.globals.set("access_token", jsonData.access_token)`

2. 正则表达式提取器 (都是从返回数据中提取)
    - `var token = responseBody.match('"access_token":"(.*?)"')`
    - `pm.globals.set("access_token", token)`

3. 从cookie中提取
    - `var csrf_token = postman.getResponseCookie('csrf_token')`

4. 从响应头里提取
    - `var types = postman.getResponseHeader('Content-Type')`

# postman的动态参数
## 接口测试中的动态参数 必须用随机数来实现
1. 内置动态参数
    - `{{$timestamp}}` 
    - `{{$randomInt}}` 0-1000随机整数
    - `{{$guid}}`随机很长的字符串
2. 自定义动态参数(在Pre-request Script) 重点
    - `var times = Date.now();pm.globals.set('times', times)`

# postman的全局变量和环境变量

# postman断言
    1. 在断言里获取全局变量必须用`pm.globals.get('times');globals['times'];globals.times;`

# 必须带请求头的接口如何测试
1. fiddler抓请求头

# postman+newman+jenkins实现自动升报告并持续集成
## postman为接口测试而生,newman为postman而生
1. 安装NODE.js
2. newman`npm install newman`
3. 导出postman的测试用例、环境变量、全局变量
4. 固定写法`newman run "e:\\yongli.json" -e "e://huanjing.json" -g "e://quanju.json" -r cli.html.json.junit --reporter-html-export "e:\\report.html"`

# 和Jenkins持续集成
1. 构建：执行windows批处理命令
2. 构建后：Publish HTML Reports