# EDITIONS
1. 歌曲名包含(Live)，并非下载首选
   - 根据第一条歌曲名是否包含Live，往后顺延
2. 下载`陈洁仪 喜欢你`第一选择没有找到下载链接
   - 新增index属性，默认为0即下载第一条，如果下载失败，index+1下载下一条节目
3. 下载`希林娜依·高 喜欢你` 下载成功但是最后会报错
   - 盲猜是因为专辑album为None最后输入数据失败导致报错，如果为None就设为''
4. 暂无


# Cautions
1. requests获得的数据，resp.text是str, resp.content是bytes
2. 