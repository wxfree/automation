# automation
1. `pip install selenium`
2. 修改下载源：`pip install pytest -i http://mirrors.aliyun.com/pypi/simple/`
3. 下载对应本机chrome浏览器版本的chromedriver,`http://npm.taobao.org/mirrors/chromedriver/`
4. 将下载的`chromedriver.exe`放到`python.exe`解释器同级目录下
5. 安装git，使用git bash, `where python/ which python`可以找到4的目录


# git on macOS how to solve `LibreSSL SSL_connect: SSL_ERROR_SYSCALL in connection to github.com:443`
1. `networksetup -setv6off Wi-Fi`
2. `networksetup -setv6automatic Wi-Fi`
