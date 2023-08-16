"""
    行情demo - 连接并登录 openctp 7x24 行情服务
"""

from openctp_tts import mdapi

# 行情前置地址 openctp 7x24 环境
md_front = 'tcp://121.37.80.177:20004'


class CMdSpiImpl(mdapi.CThostFtdcMdSpi):
    """ 回调实现类 """

    def __init__(self, _api: mdapi.CThostFtdcMdApi):
        super().__init__()
        self._api = _api

    def OnFrontConnected(self):
        """ 前置连接成功 """
        print("行情前置连接成功")

        print("登录请求")
        req = mdapi.CThostFtdcReqUserLoginField()
        self._api.ReqUserLogin(req, 0)

    def OnRspUserLogin(self, pRspUserLogin: mdapi.CThostFtdcRspUserLoginField,
                       pRspInfo: mdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 登录应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print("登录失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
            return

        print("登录成功: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)


if __name__ == '__main__':
    # 实例化请求类
    api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")  # type: mdapi.CThostFtdcMdApi
    print("TTS行情API版本号:", api.GetApiVersion())
    # 实例化回调实现类
    spi = CMdSpiImpl(api)
    # 请求实例注册行情前置地址
    api.RegisterFront(md_front)
    # 请求实例注册回调实例
    api.RegisterSpi(spi)
    # 初始化请求实例
    api.Init()

    print("Press Enter key to exit ...")
    # 阻塞主线程，等待 连接、认证、登录
    input()

    # 释放实例
    api.Release()
