# from Monitoring import monitoring
import sched
import time
import pytz
from datetime import datetime, timedelta
s = sched.scheduler(time.time, time.sleep)
# Lite monitoring every hour from 09:00 - 21:00 Greek time on working days
# Deep monitoring at the end of each day


def calculate_delay(start):           # return delay in seconds
    return (start - datetime.now(pytz.timezone('Europe/Athens'))).total_seconds()


def scheduling(start, end):
    # Plan for next monitoring
    now = datetime.now(pytz.timezone('Europe/Athens'))
    next_hour = now + timedelta(hours=1)                                                            # Monitoring in one hour
    delay = calculate_delay(next_hour)                                                              # I have "delay" seconds until then
    # print(now>end)
    if now > end:                                                                                   # No more monitoring for today
        new_day_start, new_day_end = perform_checks(now, start, end)                                # Check the new day start and end
        print("Next monitoring: ", new_day_start)
        s.enter(calculate_delay(new_day_start), 1, scheduling, (new_day_start, new_day_end,))       # call me on new day's start
    else:                                   
        print("Next monitoring in one hour")
        s.enter(delay, 1, scheduling, (start, end,))                                                # call monitoring again in an hour
    # Do the monitoring
    print("Execute monitoring: ", now)


def perform_checks(athens_now, start, end):                                                         # Check if will be done today or Start day is in the weekend
    """print("Start is: ", end='')
    print(start)
    print("End is: ", end='')
    print(end)
    print("Athens now: ", end='')
    print(athens_now)"""
    offset = 0                                                                                      # we do not expect a different start datetime
    start_day = start.strftime("%a")                                                                # What day is it today?
    # print("Start day is "+start_day)
    if start_day == "Sat":
        offset += 2                                                                                 # Skip today and tomorrow
    if start_day == "Sun":
        offset += 1                                                                                 # Skip today
    if offset == 0 and athens_now > start:                                                          # It is not weekend AND we are late
        # print("In")
        new_start = start + timedelta(days=1)                                                       # then provisional start is tomorrow
        new_end = end + timedelta(days=1)
        perform_checks(athens_now, new_start, new_end)                                              # Check tomorrow as well
        return new_start, new_end
    # print("Offset: "+str(offset))
    new_start = start + timedelta(days=offset)                                                      # Update start and end datetimes with the right offset
    new_end = end + timedelta(days=offset)
    return new_start, new_end


# Setting Start and End date times
athens_datetime_now = datetime.now(pytz.timezone('Europe/Athens'))                                  # Current time in Athens, Greece
start_datetime = athens_datetime_now.replace(hour=9, minute=00, second=00)                          # Provisional start datetime
end_datetime = athens_datetime_now.replace(hour=21, minute=00, second=00)                           # Provisional end datetime

start_datetime, end_datetime = perform_checks(athens_datetime_now, start_datetime, end_datetime)    # Finalize the start and end datetimes
# print("Start datetime: "+str(start_datetime))
# print("End datetime: "+str(end_datetime))

# Calculate waiting time until monitoring
delay = calculate_delay(start_datetime)
wait = str(timedelta(seconds=delay))
print("Start monitoring in "+wait+" (H:m:s)")

# Activate the scheduling
s.enter(calculate_delay(start_datetime), 1, scheduling, (start_datetime, end_datetime,))
s.run()
