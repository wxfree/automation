# pytest
0. `https://www.bilibili.com/video/BV14i4y1c7Jo/?spm_id_from=333.788.recommend_more_video.0`
1. pytest是一个非常成熟的python单元框架，比unittest更灵活，容易上手
2. pytest可以和selenium、requests、appium结合实现web自动化、接口自动化、app自动化
3. pytest可以实现测试用例的跳过以及reruns失败用例重试
   - `--last-failed`, 如果run的时候跟这个参数只会运行上次失败的用例，这就解决了上面说的需求。
   - `--failed-first`，如果run的时候跟这个参数会先运行上次失败的case，然后再run其余的case。
   - `--cache-show`，跟上个参数，会显示上次run的信息。
   - `--cache-clear`, 在run前先把之前的cache清除。
   - `python -m pytest cases -k 0000`选择性
4. pytest可以和allure生成非常美观的测试报告
5. 可以和jenkins持续集成
6. 有很多强大的插件
    - `pytest`
    - `pytest-html`
    - `pytest-xdist`(测试用例分布式执行，多cpu分发),`pytest -n 2`多线程执行(貌似没比单线程快呀)
    - `pytest-ordering`(用于改变测试用例的执行顺序),`@pytest.mark.run(order=1)`按顺序执行用例
    - `pytest-rerunfailures`(用例失败后重跑),`pytest --reruns 2`失败之后立即重新跑该用例2次
    - `allure-pytest`
   6.1 将所有的插件名按行放入`requirements.txt`中，通过`pip install -r requirements.txt`安装
7. 使用方法(默认的测试用例规则以及基础应用)
   - 模块名必须以`test_`开头或者以`_test`结尾
   - 测试类必须以Test开头，并且不能用__init__方法
   - 测试方法必须以test开头
8. 测试用例的运行方式
   > 主函数模式: 
     - 运行所有：`pytest.main(['-s'])`
     - 指定模块：`pytest.main(['-sv', 'test_login.py'])`
     - 指定目录：`pytest.main(['-sv','./cases'])`
     - 通过nodeid
   
   > 命令行模式:
   - `python -m pytest cases -sv -n 2 --max-failed 2`

   > 通过读取pytest.ini配置文件运行:
   - 位置：一般放在项目的根目录
   - 编码：必须是ANSI,可以使用notepad++修改编码格式(这个好像不一定)
   - 作用：改变pytest默认行为
   - 运行的规则：都会读取这个配置文件

   > 参数详解
   - `-s`输出调试信息，包括打印的信息;`-v`显示更详细的信息
   - `-n 2`两个线程跑,`--max-fail=2`出现两次用例失败就停止,`-x 1`出现1次用例失败立即停止