from jqdatasdk import *
auth('15825675534','ASd159357123!')

df1 = get_price('000001.XSHE', count = 2, end_date='2020-04-29', frequency='daily', fields=['volume', 'money'])