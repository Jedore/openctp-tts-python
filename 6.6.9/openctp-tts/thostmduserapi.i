%module(directors="1") thostmduserapi
%{
#include "ThostFtdcMdApi.h"
#include <codecvt>
#include <locale>
#include <vector>
#include <string>
using namespace std;
#ifdef _MSC_VER
const static locale g_loc("zh-CN");
#else    
const static locale g_loc("zh_CN.GB18030");
#endif
%}

%feature("python:annotations", "c");
%feature("director") CThostFtdcMdSpi;

%typemap(out) char[ANY], char[] {
    const std::string &gbk($1);
    std::vector<wchar_t> wstr(gbk.size());
    wchar_t* wstrEnd = nullptr;
    const char* gbEnd = nullptr;
    mbstate_t state = {};
    int res = use_facet<codecvt<wchar_t, char, mbstate_t>>
        (g_loc).in(state,
            gbk.data(), gbk.data() + gbk.size(), gbEnd,
            wstr.data(), wstr.data() + wstr.size(), wstrEnd);
 
    if (codecvt_base::ok == res)
    {
        wstring_convert<codecvt_utf8<wchar_t>> cutf8;
        std::string result = cutf8.to_bytes(wstring(wstr.data(), wstrEnd));       
        resultobj = SWIG_FromCharPtrAndSize(result.c_str(), result.size()); 
    }
    else
    {
        std::string result;
        resultobj = SWIG_FromCharPtrAndSize(result.c_str(), result.size()); 
    }
}
%typemap(in) char *[] {
  /* Check if is a list */
  if (PyList_Check($input)) {
    int size = PyList_Size($input);
    int i = 0;
    $1 = (char **) malloc((size+1)*sizeof(char *));
    for (i = 0; i < size; i++) {
      PyObject *o = PyList_GetItem($input, i);
      if (PyString_Check(o)) {
        $1[i] = PyString_AsString(PyList_GetItem($input, i));
      } else {
        free($1);
        PyErr_SetString(PyExc_TypeError, "list must contain strings");
        SWIG_fail;
      }
    }
    $1[i] = 0;
  } else {
    PyErr_SetString(PyExc_TypeError, "not a list");
    SWIG_fail;
  }
}

// This cleans up the char ** array we malloc'd before the function call
%typemap(freearg) char ** {
  free((char *) $1);
}

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
%include "ThostFtdcMdApi.h"
