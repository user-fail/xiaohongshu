## 声明
> 本仓库的所有内容仅供学习和参考之用，禁止用于商业用途。任何人或组织不得将本仓库的内容用于非法用途或侵犯他人合法权益。本仓库所涉及的爬虫技术仅用于学习和研究，不得用于对其他平台进行大规模爬虫或其他非法行为。对于因使用本仓库内容而引起的任何法律责任，本仓库不承担任何责任。使用本仓库的内容即表示您同意本免责声明的所有条款和条件。
## 原理
利用playwright远程调试咕噜咕噜(google)浏览器获取note_id,本地跑接口，采用单线程 。
## 使用
**配置环境**
```angular2html
pip install -r requirements.txt
```
**启动咕噜咕噜(google)**    
先登录小红书,免去模拟登录的麻烦
```angular2html
”C:\Program Files\Google\Chrome\Application\chrome.exe“ --remote-debugging-port=9222
```


**配置cookies,headers**   
get_comment.py下配置一下

##提示
抓取过程采用1到5秒进行请求一次
