> :warning: 本项目不再维护，建议使用 [openctp-ctp](https://github.com/openctp/openctp-ctp-python) 和 [openctp-ctp-channels](https://github.com/Jedore/openctp-ctp-channels) :sparkles:

<h1 align="center">openctp-tts</h1>

<div>
    <a href="#"><img src="https://flat.badgen.net/badge/os/windows-x86/cyan?icon=windows" /></a>
    <a href="#"><img src="https://flat.badgen.net/badge/os/windows-x86_64/cyan?icon=windows" /></a>
    <a href="#"><img src="https://img.shields.io/badge/os-linux_x86_64-white?style=flat-square&logo=linux&logoColor=white&color=rgb(35%2C189%2C204)" /></a>
    <a href="#"><img src="https://flat.badgen.net/badge/os/macos-x86_64/cyan?icon=apple" /></a>
    <a href="#"><img src="https://flat.badgen.net/badge/os/macos-arm64/cyan?icon=apple" /></a>
</div>
<div>
    <a href="#"><img src="https://flat.badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11|3.12/blue" /></a>
    <a href="https://pepy.tech/project/openctp-tts" ><img src="https://static.pepy.tech/badge/openctp-tts" /></a>
    <a href="#" ><img src="https://flat.badgen.net/badge/license/BSD-3/blue?" /></a>
    <a href="#" ><img src="https://flat.badgen.net/badge/test/pass/green?icon=github" /></a>
    <a href="#" ><img src="https://flat.badgen.net/badge/CI/success/green?icon=github" /></a>
</div>

<br>

:rocket:以 Python 的方式，简化对接 openctp TTS 的过程，节省精力，快速上手。

openctp TTS 提供了稳定的**7x24模拟交易平台**, 其接口 TTSAPI 完全兼容上期技术官方 CTPAPI 接口，但同样也是 C++ 版本。
本项目提供了 TTSAPI 对应的 Python 库，用于使用 Python 接入 openctp TTS 系统。

> :memo: openctp TTSAPI 详情参见 [github/openctp](https://github.com/openctp/openctp)
> 或 [openctp模拟柜台（TTS）](http://121.37.80.177:50080/Download.html)

* [支持版本](#支持版本)
* [使用方式](#使用方式)
* [代码示例](#代码示例)
* [工具脚本](#工具脚本)
* [字符集问题](#字符集问题)
* [说明](#说明)

## 支持版本

| TTSAPI(C++) | openctp-tts(python) | win x86            | win x64            | linux x64          | mac x64            | mac arm64          |
|-------------|---------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| 6.3.15      | 6.3.15.*            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.3.19_P1   | 6.3.19.*            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.5.1       | 6.5.1.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.6.1_P1    | 6.6.1.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.6.7       | 6.6.7.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.6.9       | 6.6.9.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.7.0       | 6.7.0.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.7.1       | 6.7.1.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.7.2       | 6.7.2.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |

## 使用方式

需要自行提前准备好 Python 环境, 选择一个版本安装，如 6.6.9

```shell
pip install openctp-tts==6.6.9.* -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host=pypi.tuna.tsinghua.edu.cn
```

`zsh`安装:

```shell
pip install openctp-tts==6.6.9.\* -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host=pypi.tuna.tsinghua.edu.cn
```

引用方法:

```python 
from openctp_tts import tdapi, mdapi
```

更多的接口使用方法参考 [代码示例](#代码示例)

## 代码示例

本项目提供了一些 openctp-tts 的基本使用方式及部分接口示例，具体如下:

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
    - [请求查询合约手续费率](demo/td_qry_instrument_commission_rate.py)
    - [请求查询行情](demo/td_qry_depth_market_data.py)

**代码示例仅仅作为参考，只是完成 openctp-tts 库及 ttsapi 接口本身的功能，未考虑项目及工程性场景逻辑，
若要将 openctp-tts 引入项目，勿照搬示例代码。**

## 工具脚本

- [ttsping](tools/ttsping.py) 检查前置服务是否可正常连接

## 字符集问题

Linux下安装后，需要安装中文字符集，否则导入时报错：

```text
>>> import openctp_tts
terminate called after throwing an instance of 'std::runtime_error'
what():  locale::facet::_S_create_c_locale name not valid
Aborted
```

需要安装 `GB18030` 字符集，这里提供 ubuntu/debian/centos 的方案：

```bash
# Ubuntu (20.04)
sudo apt-get install -y locales
sudo locale-gen zh_CN.GB18030

# Debian (11)
sudo apt install locales-all
sudo localedef -c -f GB18030 -i zh_CN zh_CN.GB18030

# CentOS (7)
sudo yum install -y kde-l10n-Chinese
sudo yum reinstall -y glibc-common
```

## 说明

- 限于时间/精力有限，只是在 openctp 7x24 模拟平台进行了简单的测试
- 后续会完善更多的测试
- [更新日志](CHANGELOG.md)
