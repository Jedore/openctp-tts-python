%module(directors="1") thosttraderapi
%{
#include "ThostFtdcTraderApi.h"
#include "iconv.h"
%}
%typemap(out) char[ANY], char[] {
    if ($1) {
        iconv_t conv = iconv_open("UTF-8", "GBK");
        if (conv == (iconv_t)-1) {
            PyErr_SetString(PyExc_RuntimeError, "failed to initialize iconv.");
            SWIG_fail;
        } else {
            size_t inlen = strlen($1);
            size_t outlen = 4096;
            char buf[4096];
            char **in = &$1;
            char *out = buf;

            if (iconv(conv, in, &inlen, &out, &outlen) != (size_t)-1) {
                iconv_close(conv);
                $result = SWIG_FromCharPtrAndSize(buf, sizeof buf - outlen);
            } else {
                iconv_close(conv);
                PyErr_SetString(PyExc_UnicodeError, "failed to convert '$1_name' from GBK to UTF-8.");
                SWIG_fail;
            }
        }
    }
}

%feature("director") CThostFtdcTraderSpi;
%ignore THOST_FTDC_VTC_BankBankToFuture;
%ignore THOST_FTDC_VTC_BankFutureToBank;
%ignore THOST_FTDC_VTC_FutureBankToFuture;
%ignore THOST_FTDC_VTC_FutureFutureToBank;
%ignore THOST_FTDC_FTC_BankLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BrokerLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BankLaunchBrokerToBank;
%ignore THOST_FTDC_FTC_BrokerLaunchBrokerToBank;
%feature("director") CThostFtdcTraderSpi;
%include "ThostFtdcUserApiDataType.h"
%include "ThostFtdcUserApiStruct.h"
%include "ThostFtdcTraderApi.h"
