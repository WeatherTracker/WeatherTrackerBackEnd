from Data.CWS_7Days import Get_7Days_Data
from Data.CWS_3Days import Get_3Days_Data
import threading
# from Data.PM2_5 import Get_PM2_5Data
import schedule
import time
def update():
    schedule.every().day.at('21:32').do(Get_3Days_Data,0)
    schedule.every().day.at('21:32').do(Get_7Days_Data,0)
    # schedule.every().day.at('17:42').do(Get_PM2_5Data)
    while True:
        schedule.run_pending()
        time.sleep(1)