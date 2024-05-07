# from datetime import datetime, timedelta
#
# def generate_time_slots(start_time, end_time, slot_duration):
#     current_time = start_time
#     slot=[]
#     while current_time < end_time:
#         slot.append(str(current_time).split(" ")[1][:5]+" to "+str(current_time+slot_duration).split(" ")[1][:6])
#         current_time += slot_duration
#     return (slot)
# start_time = datetime.strptime("08:00", "%H:%M")
# end_time = datetime.strptime("18:00", "%H:%M")
# slot_duration = timedelta(minutes=20)
# generate_time_slots(start_time, end_time, slot_duration)
# # for time_slot in generate_time_slots(start_time, end_time, slot_duration):
# #     print(time_slot.strftime("%H:%M"))


import calendar

def get_dates(year, month):
    _, num_days = calendar.monthrange(year, month)
    dates = [f"{year}-{month:02d}-{day:02d}" for day in range(1, num_days + 1)]
    return dates

year = 2024
month = 3
dates = get_dates(year, month)
print("Dates in March 2024:")
for date in dates:
    print(date)