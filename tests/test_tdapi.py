from queue import Queue

from openctp_tts import tdapi as api

Q_CONNECT = Queue(maxsize=1)
Q_AUTH = Queue(maxsize=1)

TIMEOUT = 5  # seconds

USER = '209025'


class CTdSpiImpl(api.CThostFtdcTraderSpi):
    def __init__(self, tdapi):
        super().__init__()
        self.tdapi = tdapi

    def OnFrontConnected(self):
        Q_CONNECT.put(True, timeout=TIMEOUT)
        req = api.CThostFtdcReqAuthenticateField()
        req.BrokerID = '9999'
        req.UserID = USER
        req.AppID = 'simnow_client_test'
        req.AuthCode = '0000000000000000'
        self.tdapi.ReqAuthenticate(req, 0)

    def OnRspAuthenticate(self,
                          pRspAuthenticateField: api.CThostFtdcRspAuthenticateField,
                          pRspInfo: api.CThostFtdcRspInfoField, nRequestID: int,
                          bIsLast: bool):
        if pRspInfo is None or pRspInfo.ErrorID == 0:
            # success
            Q_AUTH.put(True, timeout=TIMEOUT)
        else:
            # failed
            Q_AUTH.put(False, timeout=TIMEOUT)


def test_mdapi():
    td_front = 'tcp://121.37.80.177:20002'
    try:
        tdapi = api.CThostFtdcTraderApi.CreateFtdcTraderApi(USER)
        tdspi = CTdSpiImpl(tdapi)
        tdapi.RegisterSpi(tdspi)
        tdapi.RegisterFront(td_front)
        tdapi.Init()

        try:
            Q_CONNECT.get(timeout=TIMEOUT)
        except:
            assert False, 'Connect Failed!'

        try:
            if not Q_AUTH.get(timeout=TIMEOUT):
                assert False, 'Auth Failed!'

        except:
            assert False, 'Auth Failed!'

    except AssertionError as e:
        error = str(e)
