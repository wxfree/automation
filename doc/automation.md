1. 了解你有没有自动化测试项目的实战经验
    - 有没有做过自动化测试
    - 请举例说明下，你在编写自动化脚本过程中碰到了哪些异常
        - NoSuchElementException、TimeoutException、NoSuchFrameException
    - 是如何在公司里面实施自动化测试
2. 你在自动化领域里面的技术深度怎么样


# 接口请求
1. Accept:客户端接收的数据类型
2. X-Requested-With: 
3. User-Agent
4. Cookie: 保存在客户端的一小段的文本信息
5. Referer
6. Content-Type:

# 接口测试流程和方案
1. 拿到api文档(规范文档:swagger/showdoc)
    - 头疼的面试题?在你们的项目中测了什么接口、登陆、注册接口、查询用户信息接口等等
2. 编写接口测试计划和方案(接口怎么测)
    - 正例: 输入正常参数, 接口正常返回
    - 反例: 
        - 鉴权反例,鉴权码为空/过期/错误
        - 参数反例,参数为空、类型错误、长度异常、错误码异常
        - 其他场景,接口黑名单、接口调佣次数、接口分页(0、1、中间页、最后一页)、根据业务来定
3. 编写测试接口用例
4. 使用接口测试工具执行接口测试
5. 输出接口测试报告(HTML格式)

# 接口测试工具
1. postman+newman+git+jenkins
2. jmeter+ant+git+jenkins、ant是jmeter插件
3. soupui、apihost、fiddler、charles
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


# httprunner
1. 安装`pip install httprunner`
2. 必须知道的五个httprunner的命令
    - httprunner 主命令 用于所有功能
    - hrun 用于运行yaml/json/pytest测试用例
    - hmake 用于将yaml/json测试用例转化成pytest文件
    - har2case 用于将har文件转化成yaml/json/pytest测试用例
    - locust 用于性能测试 bnd21



# UI自动化测试
1. 元素定位-最初级的自动化
    - 元素无法定位的原因
        - 