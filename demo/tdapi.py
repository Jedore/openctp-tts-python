"""
    交易API demo
"""
import random

from openctp_ctp import tdapi


class CTdSpiImpl(tdapi.CThostFtdcTraderSpi):
    def __init__(self, tdapi):
        super().__init__()
        self.tdapi = tdapi

    def OnFrontConnected(self):
        """ 前置连接成功 """
        print("OnFrontConnected")
        req = tdapi.CThostFtdcReqAuthenticateField()
        req.BrokerID = brokerid
        req.UserID = user
        req.AppID = appid
        req.AuthCode = authcode
        self.tdapi.ReqAuthenticate(req, 0)

    def OnFrontDisconnected(self, nReason: int):
        """ 前置断开 """
        print("OnFrontDisconnected: nReason=", nReason)

    def OnRspAuthenticate(self, pRspAuthenticateField: tdapi.CThostFtdcRspAuthenticateField,
                          pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 客户端认证应答 """
        if pRspInfo is not None:
            print(f"OnRspAuthenticate: ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}")

        if pRspInfo is None or pRspInfo.ErrorID == 0:
            req = tdapi.CThostFtdcReqUserLoginField()
            req.BrokerID = brokerid
            req.UserID = user
            req.Password = password
            req.UserProductInfo = "openctp"
            self.tdapi.ReqUserLogin(req, 0)

    def OnRspUserLogin(self, pRspUserLogin: tdapi.CThostFtdcRspUserLoginField,
                       pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 登录应答 """
        print(f"OnRspUserLogin: ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}, "
              f"TradingDay={pRspUserLogin.TradingDay}")


if __name__ == '__main__':
    td_front = 'tcp://121.37.80.177:20002'
    # user/password 需要更换为自己的
    user = 'user'
    password = 'password'
    brokerid = '9999'
    authcode = '0000000000000000'
    appid = 'simnow_client_test'

    td_api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi(user)
    print("ApiVersion: ", td_api.GetApiVersion())
    td_spi = CTdSpiImpl(td_api)
    td_api.RegisterSpi(td_spi)
    td_api.SubscribePrivateTopic(tdapi.THOST_TERT_QUICK)
    td_api.SubscribePublicTopic(tdapi.THOST_TERT_QUICK)
    td_api.RegisterFront(td_front)
    td_api.Init()

    print("press Enter key to exit ...")
    input()
