# automation
1. `pip install selenium`
2. 修改下载源：`pip install pytest -i http://mirrors.aliyun.com/pypi/simple/`
3. 下载对应本机chrome浏览器版本的chromedriver,`http://npm.taobao.org/mirrors/chromedriver/`
4. 将下载的`chromedriver.exe`放到`python.exe`解释器同级目录下
5. 安装git，使用git bash, `where python/ which python`可以找到4的目录


# Problems
1. git on macOS how to solve `LibreSSL SSL_connect: SSL_ERROR_SYSCALL in connection to github.com:443`
    - `networksetup -setv6off Wi-Fi`
    - `networksetup -setv6automatic Wi-Fi`
    
2. git on win10 how to solve `OpenSSL SSL_read: Connection was reset, errno 10054`
    - open cmd, use `ipconfig /flushdns`
    
3. git on win10 how to solve `Author identity unknown`
    - `cd .git`
    - `git config user.name 'wxfree'`
    - `git config user.email '383175243@163.com'`
    
