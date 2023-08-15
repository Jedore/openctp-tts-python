"""
    TTS 通讯链路检测工具, 用于检测交易/行情前置地址是否正常

参考 c++ ctpping https://github.com/openctp/openctp/tree/master/demo/ctpping
使用前安装 openctp-tts: pip install openctp-tts
用法: python ttsping.py address
示例: python ttsping.py tcp://121.37.90.193:20002

正常输出:
   version: V6_6_9
   connected.
   response time: 27 milliseconds
异常输出:
   version: V6_6_9
   time out.
"""

import sys
import time
from queue import Queue, Empty

from openctp_tts import mdapi

Q_EXIT = Queue(maxsize=1)


class CMarketSpi(mdapi.CThostFtdcMdSpi):
    def __init__(self, _api: mdapi.CThostFtdcMdApi):
        super().__init__()

        self._api = _api
        self._start_time = None
        self._end_time = None

    def OnFrontConnected(self):
        print("connected.")

        self._start_time = int(time.time() * 1000)
        self._api.ReqUserLogin(mdapi.CThostFtdcReqUserLoginField(), 0)

    def OnFrontDisconnected(self, nReason: int):
        print("disconnected.")
        Q_EXIT.put_nowait(None)

    def OnRspUserLogin(
            self,
            pRspUserLogin: mdapi.CThostFtdcRspUserLoginField,
            pRspInfo: mdapi.CThostFtdcRspInfoField,
            nRequestID: int,
            bIsLast: bool,
    ):
        self._end_time = int(time.time() * 1000)
        print("response time:", self._end_time - self._start_time, "milliseconds")
        Q_EXIT.put_nowait(None)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:\n\tpython ttsping.py <tts md/td front address>")
        print("Example:\n\tpython ttsping.py tcp://121.37.90.193:20002")
        exit(0)

    print("TTSAPI版本号:", mdapi.CThostFtdcMdApi.GetApiVersion())
    api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi()
    spi = CMarketSpi(api)
    api.RegisterFront(sys.argv[1])
    api.RegisterSpi(spi)
    api.Init()

    try:
        Q_EXIT.get(timeout=5)
    except Empty:
        print("time out.")
    finally:
        api.Release()
