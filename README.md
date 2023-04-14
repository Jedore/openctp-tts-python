<h1 align="center">openctp-tts</h1>

<p align="center">     
    <a href="#" target="_blank">
        <img src="https://badgen.net/badge/tts/6.3.15|6.3.19|6.5.1|6.6.1|6.6.7|6.6.9/cyan" />
    </a>       
    <a href="#">         
        <img src="https://badgen.net/badge/platform/windows|linux|macos/cyan" />  
    </a>        
</p>

<p align="center">  
    <a href="https://pypi.org/project/openctp-tts" target="_blank">                                    
        <img src="https://badgen.net/badge/pypi/openctp-tts/blue" />               
    </a> 
    <a href="#">     
        <img src="https://badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11/blue" />          
    </a> 
    <a href="https://github.com/Jedore/openctp-tts-python/actions" target="_blank">                                                      
        <img src="https://badgen.net/badge/CI-Test/passing/green?icon=github" />                         
    </a> 
    <a href="https://github.com/Jedore/openctp-tts-python/blob/main/LICENSE" target="_blank">                                                               
        <img src="https://badgen.net/badge/license/MIT/green" />                              
    </a> 
</p>

<p align="center">          
    :rocket:<em>以 Python 的方式，简化对接 TTS 的过程，节省精力，快速上手</em>  
</p>

-----

## 安装:hammer_and_wrench:

```shell
# pip install openctp-tts==<ctpapi version>
pip install openctp-tts==6.3.15
pip install openctp-tts==6.6.7
```

## 代码示例:man_technologist:

```python
from openctp_tts import mdapi, tdapi

md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")
td_api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi('user_id')
```

- 行情 [demo](demo/mdapi.py)
- 交易 [demo](demo/tdapi.py)

## 功能:full_moon_with_face:

- 支持多版本 TTS
    - 6.3.15_20190220
    - 6.3.19_P1_20200106
    - 6.5.1_20200908
    - 6.6.1_P1_20210406
    - 6.6.7_20220613
    - 6.6.9_20220920
- 支持多版本 Python (3.7 ~ 3.11)
- 支持多平台
    - Windows
    - Linux
    - Macos

## 核心逻辑:art:

利用 [SWIG](https://www.swig.org/)及 TTS 库生成Python扩展库

```mermaid 
graph TD;     
  PythonApp<-->Python扩展;     
  Python扩展<-->TTS库;     
  TTS库<-->Simnow前置;     
```

## 更多信息:page_facing_up:

- [openctp](https://github.com/openctp/openctp)
- QQ交流群

    <img src="https://user-images.githubusercontent.com/17944025/231727684-fb62f5f9-71d8-448f-9e35-255639756bb2.png" width="200px">
