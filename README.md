<h1 align="center">OPENCTP-TTS</h1>

<p align="center">          
    <em>:rocket:以 Python 的方式，简化对接 TTS 的过程，节省精力，快速上手</em>  
</p>

<p align="center">     
    <a href="https://pypi.org/project/openctp-tts" target="_blank">                  
        <img src="https://badgen.net/badge/pypi/openctp-tts/green" />     
    </a>     
    <a href="#" target="_blank">
        <img src="https://badgen.net/badge/tts/6.3.15|6.3.19|6.5.1|6.6.1|6.6.7|6.6.9/green" />
    </a>       
    <a href="#">     
        <img src="https://badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11/green" />          
    </a> 
    <a href="#">         
        <img src="https://badgen.net/badge/plat/Windows|Linux|Mac/green" />  
    </a>        
</p>

## 安装

```shell
pip install openctp-tts==6.3.15.*
pip install openctp-tts==6.3.19.*
pip install openctp-tts==6.5.1.*
pip install openctp-tts==6.6.1.*
pip install openctp-tts==6.6.7.*
pip install openctp-tts==6.6.9.*
```

## 代码示例

```python
from openctp_tts import mdapi, tdapi

md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")
td_api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi('user_id')
```

- 行情 [demo](demo/mdapi.py)
- 交易 [demo](demo/tdapi.py)

## 功能

- 支持多版本 TTS
    - 6.3.15_20190220
    - 6.3.19_P1_20200106
    - 6.5.1_20200908
    - 6.6.1_P1_20210406
    - 6.6.7_20220304
    - 6.6.9_20220920
- 支持多版本 Python (3.7 ~ 3.11)
- 支持多平台
    - Windows x64
    - Linux x64
    - Mac x64 arm64

## 其他说明

- 关于TTS更多的信息参见 [openctp](https://github.com/openctp/openctp)
- [更新日志](CHANGELOG.md)
