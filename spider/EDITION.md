# EDITIONS
1. 歌曲名包含(Live)，并非下载首选
   - 根据第一条歌曲名是否包含Live，往后顺延
2. 下载`陈洁仪 喜欢你`第一选择没有找到下载链接
   - 新增index属性，默认为0即下载第一条，如果下载失败，index+1下载下一条节目
3. 下载`希林娜依·高 喜欢你` 下载成功但是最后会报错
   - 盲猜是因为专辑album为None最后输入数据失败导致报错，如果为None就设为''
4. 2021-08-11，新建`kuwo.py`不再使用webdriver来获取歌曲关键属性，而是从接口直接获取
   - `kings & Queens`无法直接下载，webdriver方式可以
      - requests请求时，添加的参数不需要转码
5. 学习如何打日志！   



# Cautions
1. requests获得的数据，resp.text是str, resp.content是bytes
2. requests.get(url, params={'key':'kings & queens'}),此处参数不需要编码