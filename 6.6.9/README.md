# openctp-ctp

[![PyPI - Python Version](https://badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11/blue)](https://pypi.org/project/openctp-ctp-CTP_VERSION)

-----

## Installation

```console
pip install openctp-ctp==6.3.15
pip install openctp-ctp==6.3.19
pip install openctp-ctp==6.5.1
pip install openctp-ctp==6.6.1
pip install openctp-ctp==6.6.7
pip install openctp-ctp==6.6.9
```

## Example

[Demo](https://github.com/openctp/openctp-ctp-python/tree/main/demo)

```python
from openctp_ctp import mdapi, tdapi

md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")
td_api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi('user_id')
```

## License

`openctp-ctp` is distributed under the terms of
the [BSD-3-Clause](https://github.com/openctp/openctp-ctp-python/blob/main/LICENSE) license.

