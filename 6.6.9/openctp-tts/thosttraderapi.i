%module(directors="1") thosttraderapi
%{
#include "ThostFtdcTraderApi.h"
#include <codecvt>
#include <locale>
#include <vector>
#include <string>
using namespace std;
#ifdef _MSC_VER
const static locale g_loc("zh-CN");
#else
const static locale g_loc("zh_CN.GB18030");
#endif %}
%typemap(out) char[ANY], char[] {
    const std::string &gbk($1);
    std::vector<wchar_t> wstr(gbk.size());
    wchar_t* wstrEnd = nullptr;
    const char* gbEnd = nullptr;
    mbstate_t state = {};
    int res = use_facet<codecvt<wchar_t, char, mbstate_t>> (g_loc).in(state, gbk.data(), gbk.data() + gbk.size(), gbEnd, wstr.data(), wstr.data() + wstr.size(), wstrEnd);
    if (codecvt_base::ok == res) {
        wstring_convert<codecvt_utf8<wchar_t>> cutf8;
        std::string result = cutf8.to_bytes(wstring(wstr.data(), wstrEnd));
        resultobj = SWIG_FromCharPtrAndSize(result.c_str(), result.size());
    } else {
        std::string result;
        resultobj = SWIG_FromCharPtrAndSize(result.c_str(), result.size());
    }
}
%feature("python:annotations", "c");
%feature("director") CThostFtdcTraderSpi;
%feature("director") CThostFtdcTraderSpi;
%ignore THOST_FTDC_VTC_BankBankToFuture;
%ignore THOST_FTDC_VTC_BankFutureToBank;
%ignore THOST_FTDC_VTC_FutureBankToFuture;
%ignore THOST_FTDC_VTC_FutureFutureToBank;
%ignore THOST_FTDC_FTC_BankLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BrokerLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BankLaunchBrokerToBank;
%ignore THOST_FTDC_FTC_BrokerLaunchBrokerToBank;

%include "ThostFtdcUserApiDataType.h"
%include "ThostFtdcUserApiStruct.h"
%include "ThostFtdcTraderApi.h"