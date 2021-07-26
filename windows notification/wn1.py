from win10toast import ToastNotifier

# One-time initialization
toaster = ToastNotifier()

# Show notification whenever needed
toaster.show_toast("Notification!", "Fill the timesheet!", threaded=True,
                   icon_path=None, duration=10)  # 3 seconds

# To check if any notifications are active,
# use `toaster.notification_active()`
# import time
# while toaster.notification_active():
#     time.sleep(10)