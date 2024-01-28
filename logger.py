import win32evtlogutil
import win32evtlog
import sys
import time

print("Python {0} on {1}".format(sys.version, sys.platform))

# Define your custom event source
App_Name = "Network Test"
App_Event_Id = 10001
App_Event_Category = 90
App_Event_Type = win32evtlog.EVENTLOG_INFORMATION_TYPE

# Call this function to log an event with the specified details
def log_message(message):
    if isinstance(message, str):
        win32evtlogutil.ReportEvent(
            App_Name,
            App_Event_Id,
            App_Event_Category,
            App_Event_Type,
            strings=[message],
            data=None,
        )

# def main():
#     n = 0
#     while True:
#         n += 1
#         log_message(f'Loop count {n}')
#         current_time = time.strftime('%m-%d-%Y - %H:%M:%S%p')
#         log_message(current_time)
#         time.sleep(10)

# if __name__ == "__main__":
#     main()
