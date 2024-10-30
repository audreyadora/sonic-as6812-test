
import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def datetimeToStr(dt, fmt=DATE_FORMAT):
   return dt.strftime(fmt)

def strToDatetime(s, fmt=DATE_FORMAT):
   return datetime.datetime.strptime(s, fmt)

def epochToDatetime(epoch):
   return datetime.datetime.fromtimestamp(epoch)
