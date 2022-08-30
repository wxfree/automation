1. 了解你有没有自动化测试项目的实战经验
    - 有没有做过自动化测试
    - 请举例说明下，你在编写自动化脚本过程中碰到了哪些异常
        - NoSuchElementException、TimeoutException、NoSuchFrameException
    - ☆☆☆☆是如何在公司里面实施自动化测试
        - 1-项目自动化可行性分析, 自动化率能够实施到什么程度
        - 适合做自动化的: 项目周期比较长的(一年以上)、需求不会频繁变更、自动化脚本能够持续反复使用
        - 2-自动化工具selenium、robotframework调研以及demo演示
        - 3-由leader搭建自动化测试框架，并且在项目中逐步实施，发现框架的问题并逐步改善
        - 4-把项目流程化，框架出使用文档和规范文档
        - 5-生成定制报告。并继续完善框架
2. 你在自动化领域里面的技术深度怎么样
    - ☆☆☆☆☆ 有从0开始独立搭建过接口自动化测试框架
    - 回答:在合筑空间项目搭建的接口自动化框架所使用的

# 接口请求
1. Accept:客户端接收的数据类型
2. X-Requested-With: 
3. User-Agent
4. Cookie: 保存在客户端的一小段的文本信息
5. Referer
6. Content-Type:

# 接口测试流程和方案
## ☆☆一个接口会设计多少个测试用例 一般20-30比较合适
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
# ☆☆☆☆☆postman接口关联 接口依赖☆
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
        - 定位元素的表达式错误
        - 定位元素还未加载完毕
        - 元素特殊属性
        - 元素在iframe中或者在别的window中

# 软件测试必问
1. 自我介绍
    - 你好 我叫王欣 毕业于华东理工大学 现就职于名筑信息 担任自动化测试工程师  主要负责合筑空间web项目的自动化测试框架的开发 是一个使用POM设计方法对pytest+selenium框架进行二次封装，整合了logging日志并生成allure定制报告的框架 个人比较擅长使用postman接口测试工具或requests进行接口测试 我本人比较乐观开朗有责任心，喜欢自己研究技术 谢谢，上述就是我的个人情况

2. 说下你们公司的测试流程
    - 

3. 提了一个bug 但是开发认为不是bug，作为测试你怎么办
    - 首先确认开发的环境与测试环境是否一致，并确保双方对需求的理解是一致的。然后将bug重现展示给开发看，如果bug等级较严重，开发仍然不认为是bug，就找上级或产品介入。如果是小问题，就找时间集中跟开发跟进修改

4. 对于复现率不高的bug怎么处理
    - 对于偶然出现的bug也要提交到缺陷管理平台，并将bug出现的步骤、环境、账号、操作系统等信息描述清楚，标明偶现。之后在每轮回归测试时都要尽可能复现这个bug、如果多轮回归测试都不能重现，就根据bug严重等级来确定是否要继续跟进还是关闭

5. 给你个新项目 你怎么开展测试
    - 拿到项目后，先熟悉需求 了解被测功能和各个功能的业务逻辑
    - 针对需要测试的内容进行大致的测试规划，然后细化设计每个测试用例。对功能有疑问的及时跟产品/开发讨论
    - 拿到被测软件后就按照用例自行测试，有bug就提交并跟踪

6. 说说你的职业规划
    - 希望短期内熟悉公司的业务流程，能够独立开发一个自动化测试框架，并在3年内成为一个合格的测试开发工程师

7. 如何制定一个测试计划
    - 

8. 持续集成
    - 持续集成的一般做法 1.通过git或其他版本管理工具拉取代码 2. 自动化构建-自动化编译-自动化测试-自动化部署-自动发布-自动发送邮件通知相关负责人
    - 团队的成员经常要集成他们的工作，每次集成都会通过自动化的构建 包括编译、发布、自动化测试来验证，从而尽快发现集成后的错误，目的是为了快速的迭代并保持高质量

9. 编写自动化测试脚本时候碰到过那些异常
    - TimeoutException超时异常、NoSuchElementException、FileNotFoundException、WebdriverException

10. 如何在公司实施自动化测试
    - 1.分析项目实施自动化的可行性（适合做自动化的项目:周期比较长、需求不会频繁更迭）
    - 2.自动化测试工具selenium、robotframework调研和demo演示
    - 3.由leader搭建自动化测试框架，并逐步在项目中实施，发现框架问题并逐步改善优化
    - 4.把项目流程化，并制定框架使用文档和规范文档
    - 5.生成定制报告，并持续改善
