# dxzy163_video_download
基于网站`https://www.dxzy163.com/`的DPlayer视频流异步下载
![4360_js_2024-01-19_18-00-34](https://github.com/CopyMasterJ/dxzy163_video_download/assets/108559018/7804f67d-daac-43f3-bf02-bebe5d8aa654)
需要通过控制台获取到视频目录的链接放入到main.py的requests请求中:
```m3u8_content = requests.get('https://www.dxzy163.com/playdata/8/4360.js?52888.01', verify=False).text```
