# openctp-tts

[![PyPI - Python Version](https://badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11/blue)](https://pypi.org/project/openctp-tts)

-----

## Installation

```console
pip install openctp-tts==6.3.15.*
pip install openctp-tts==6.3.19.*
pip install openctp-tts==6.5.1.*
pip install openctp-tts==6.6.1.*
pip install openctp-tts==6.6.7.*
pip install openctp-tts==6.6.9.*
```

## Example

[Demo](https://github.com/openctp/openctp-tts-python/tree/main/demo)

```python
from openctp_tts import mdapi, tdapi

md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")
td_api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi('user_id')
```

## License

`openctp-tts` is distributed under the terms of
the [BSD-3-Clause](https://github.com/openctp/openctp-tts-python/blob/main/LICENSE) license.

