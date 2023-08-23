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

openctp TTS 提供了稳定的7x24模拟交易平台, 完全兼容上期技术官方CTPAPI接口，但同样也是 C++ 版本。
本项目提供了TTSAPI对应的Python库，用于使用Python接入TTS系统。

## 安装

```shell
pip install openctp-tts==6.3.15.*
pip install openctp-tts==6.3.19.*
pip install openctp-tts==6.5.1.*
pip install openctp-tts==6.6.1.*
pip install openctp-tts==6.6.7.*
pip install openctp-tts==6.6.9.*
```

## Demo参考

[Demo](demo)

包含以下示例:

- 行情
    - [登录](demo/md_login.py)
    - [订阅](demo/md_subscribe.py)
- 交易
    - [登录](demo/td_login.py)
    - [投资者结算单确认](demo/td_settlement.py)
    - [查询合约](demo/td_qry_instrument.py)
    - [报单录入](demo/td_order_insert.py)
    - [报单查询](demo/td_order_query.py)
    - [报单撤销](demo/td_order_cancel.py)

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
- 限于精力有限，本项目前只进行了有限的测试，正式使用前请一定进行充分的测试。
- **使用本项目进行实盘交易的后果完全由使用者自己承担!!!**

## 常见问题

1. Linux下安装后，导入时报错
    ```text
    >>> import openctp_tts
    terminate called after throwing an instance of 'std::runtime_error'
      what():  locale::facet::_S_create_c_locale name not valid
    Aborted
    ```
   这是字符集问题，方案：
    ```bash
    # Ubuntu (20.04)
    sudo apt-get install -y locales
    sudo locale-gen zh_CN.GB18030
   
    # Debian (11)
    sudo apt install locales-all
    sudo localedef -c -f GB18030 -i zh_CN zh_CN.GB18030
   
    # CentOS (7)
    yum install -y kde-l10n-Chinese
    yum reinstall -y glibc-common
    ```
