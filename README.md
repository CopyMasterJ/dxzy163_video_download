# dxzy163_video_download
![](https://img.shields.io/badge/Python-3.12.1-green.svg) ![](https://img.shields.io/badge/requests-2.31.0-green.svg) ![](https://img.shields.io/badge/m3u8-4.0.0-green.svg) ![](https://img.shields.io/badge/anyio-4.0.0-green.svg)

### 网站官网:`https://www.dxzy163.com/`
## 介绍

基于此的DPlayer视频流异步下载
![4360_js_2024-01-19_18-00-34](https://github.com/CopyMasterJ/dxzy163_video_download/assets/108559018/7804f67d-daac-43f3-bf02-bebe5d8aa654)
需要通过控制台获取到视频目录的链接放入到main.py的requests请求中:
```
m3u8_content = requests.get('https://www.dxzy163.com/playdata/8/4360.js?52888.01', verify=False).text
```
## 运行环境
Version: Python3

## 依赖库
```pycon
 # pip freeze > requirements.txt
 pip install -r requirements.txt
```