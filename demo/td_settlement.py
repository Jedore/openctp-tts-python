"""
    交易demo - 投资者结算结果确认
"""

from openctp_tts import tdapi

from config import (
    td_fronts,
    td_front,
    user,
    password,
    broker_id,
    authcode,
    appid,
)


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

        print("投资者结算结果确认请求")
        req = tdapi.CThostFtdcSettlementInfoConfirmField()
        req.BrokerID = broker_id
        req.InvestorID = user
        self._api.ReqSettlementInfoConfirm(req, 0)

    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm: tdapi.CThostFtdcSettlementInfoConfirmField,
                                   pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 确认投资者结算结果应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print("确认投资者结算结果失败:", "ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
            return

        print("确认投资者结算结果成功:",
              "ConfirmDate:", pSettlementInfoConfirm.ConfirmDate,
              "ConfirmTime:", pSettlementInfoConfirm.ConfirmTime,
              "SettlementID:", pSettlementInfoConfirm.SettlementID,
              "AccountID:", pSettlementInfoConfirm.AccountID,
              "CurrencyID:", pSettlementInfoConfirm.CurrencyID,
              )


if __name__ == '__main__':
    # 实例化交易请求类
    api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi(user)  # type: tdapi.CThostFtdcTraderApi
    print("TTS交易API版本号:", api.GetApiVersion())
    print("交易前置:", td_fronts[td_front], td_front)
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
