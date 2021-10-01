# automation
1. `pip install selenium`
2. 修改下载源：`pip install pytest -i https://mirrors.aliyun.com/pypi/simple/`
3. 下载对应本机chrome浏览器版本的chromedriver,`http://npm.taobao.org/mirrors/chromedriver/`
4. 将下载的`chromedriver.exe`放到`python.exe`解释器同级目录下
5. 安装git，使用git bash, `where python/ which python`可以找到4的目录


# Problems
1. git on macOS how to solve `LibreSSL SSL_connect: SSL_ERROR_SYSCALL in connection to github.com:443`
    - `networksetup -setv6off Wi-Fi`
    - `networksetup -setv6automatic Wi-Fi`
    
2. git on win10 how to solve `OpenSSL SSL_read: Connection was reset, errno 10054`
    - open cmd, use `ipconfig /flushdns`
    - `git config --global --unset http(s).proxy`
    
3. git on win10 how to solve `Author identity unknown`
    - `cd .git`
    - `git config user.name 'wxfree'`
    - `git config user.email '383175243@163.com'`
   
4. selenium如何选择显式等待和隐式等待
   - 当页面爬取部分存在ajax部分刷新的内容时，使用显示等待`implicitly_wait`
   - 否则使用`WebDriver.until`
   - 在获取page_source前使用time.sleep(5)也可以拿到完整页面源代码，1秒左右即可(这个方法貌似最简单)
   
5. how to use token in git
   - Password for xxx:`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`
   - it lasts for three month
   
# About pytest
1. 如果看到`.pytest_cache`，可以执行
   - `--last-failed`, 如果run的时候跟这个参数只会运行上次失败的用例，这就解决了上面说的需求。
   - `--failed-first`，如果run的时候跟这个参数会先运行上次失败的case，然后再run其余的case。
   - `--cache-show`，跟上个参数，会显示上次run的信息。
   - `--cache-clear`, 在run前先把之前的cache清除。
