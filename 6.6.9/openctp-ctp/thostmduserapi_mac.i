%module(directors="1") thostmduserapi
%{
#include "ThostFtdcMdApi.h"
#include "iconv.h"
%}

%feature("director") CThostFtdcMdSpi;
%ignore THOST_FTDC_VTC_BankBankToFuture;
%ignore THOST_FTDC_VTC_BankFutureToBank;
%ignore THOST_FTDC_VTC_FutureBankToFuture;
%ignore THOST_FTDC_VTC_FutureFutureToBank;
%ignore THOST_FTDC_FTC_BankLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BrokerLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BankLaunchBrokerToBank;
%ignore THOST_FTDC_FTC_BrokerLaunchBrokerToBank;

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
%include "ThostFtdcUserApiDataType.h"
%include "ThostFtdcUserApiStruct.h"
%include "ThostFtdcMdApi.h"
