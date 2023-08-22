"""
    交易demo - 查询报单请求
"""

from openctp_tts import tdapi

# 交易前置地址 可以在 http://121.37.80.177:50080/detail.html 查看TTS前置地址
td_front = 'tcp://121.37.90.193:20002'

# 账号/密码 从 OpenCTP 公众号申请
user = 'xxx'
password = 'xxx'

# 以下为空即可
broker_id = ''
authcode = ''
appid = ''


class CTdSpiImpl(tdapi.CThostFtdcTraderSpi):
    """ 交易回调实现类 """

    def __init__(self, _api: tdapi.CThostFtdcTraderApi):
        super().__init__()
        self._api = _api

    def OnFrontConnected(self):
        """ 前置连接成功 """
        print("交易前置连接成功")

        # 认证请求
        req = tdapi.CThostFtdcReqAuthenticateField()
        req.BrokerID = broker_id
        req.UserID = user
        req.AppID = appid
        req.AuthCode = authcode
        self._api.ReqAuthenticate(req, 0)

    def OnFrontDisconnected(self, nReason: int):
        """ 前置断开 """
        print("交易前置连接断开: nReason=", nReason)

    def OnRspAuthenticate(self, pRspAuthenticateField: tdapi.CThostFtdcRspAuthenticateField,
                          pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 客户端认证应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print("认证失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
            return

        print("认证成功")

        if pRspInfo is None or pRspInfo.ErrorID == 0:
            # 登录请求
            req = tdapi.CThostFtdcReqUserLoginField()
            req.BrokerID = broker_id
            req.UserID = user
            req.Password = password
            req.UserProductInfo = "openctp"
            self._api.ReqUserLogin(req, 0)

    def OnRspUserLogin(self, pRspUserLogin: tdapi.CThostFtdcRspUserLoginField,
                       pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 登录应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print("登录失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg, "TradingDay=",
                  pRspUserLogin.TradingDay)
            return

        print("登录成功:", pRspUserLogin.UserID, "TradingDay=", pRspUserLogin.TradingDay)

        print("查询报单请求")

        req = tdapi.CThostFtdcQryOrderField()
        req.BrokerID = broker_id
        req.InvestorID = user
        req.UserID = user
        # 以下条件也可作为过滤条件
        # req.ExchangeID = 'CZCE' # 交易所代码
        # req.InstrumentID = 'AP310' # 合约
        # req.InsertTimeStart = '' # 开始时间
        # req.InsertTimeEnd = '' # 结束时间

        self._api.ReqQryOrder(req, 0)

    def OnRspQryOrder(self, pOrder: tdapi.CThostFtdcOrderField, pRspInfo: tdapi.CThostFtdcRspInfoField,
                      nRequestID: int, bIsLast: bool):
        """ 查询报单响应 """
        if pRspInfo and pRspInfo.ErrorID:
            print("查询报单失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
            return

        print("查询报单成功:",
              "InstrumentID:", pOrder.InstrumentID,
              "ExchangeID:", pOrder.ExchangeID,
              "FrontID:", pOrder.FrontID,
              "SessionID:", pOrder.SessionID,
              "OrderRef:", pOrder.OrderRef,
              "OrderSysID:", pOrder.OrderSysID,
              "OrderPriceType:", pOrder.OrderPriceType,
              "Direction:", pOrder.Direction,
              "CombOffsetFlag:", pOrder.CombOffsetFlag,
              "LimitPrice:", pOrder.LimitPrice,
              "VolumeTotalOriginal:", pOrder.VolumeTotalOriginal,
              "OrderStatus:", pOrder.OrderStatus,
              "InsertDate:", pOrder.InsertDate,
              "InsertTime:", pOrder.InsertTime,
              )


if __name__ == '__main__':
    # 实例化交易请求类
    api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi(user)  # type: tdapi.CThostFtdcTraderApi
    print("TTS交易API版本号:", api.GetApiVersion())
    # 实例化交易回调实现类
    spi = CTdSpiImpl(api)
    # 注册交易前置地址
    api.RegisterFront(td_front)
    # 交易请求实例 注册 交易回调实例
    api.RegisterSpi(spi)
    # 订阅私有流
    api.SubscribePrivateTopic(tdapi.THOST_TERT_QUICK)
    # 订阅公有流
    api.SubscribePublicTopic(tdapi.THOST_TERT_QUICK)
    # 初始化交易实例
    api.Init()

    # 阻塞 等待
    print("Press Enter key to exit ...")
    input()

    # 释放实例
    api.Release()
