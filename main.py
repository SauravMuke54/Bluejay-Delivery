import pandas as pd
from datetime import timedelta

def calculate_hours_difference(start_time, end_time):
    return (end_time - start_time).total_seconds() / 3600

def analyze_employee_data(data):
    # Convert string time to datetime format
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
    data['Time Out'] = pd.to_datetime(data['Time Out'], errors='coerce')

    # Condition (a): Employees who have worked for 7 consecutive days
    consecutive_days_result = []
    for name, group in data.groupby('Employee Name'):
        group['Consecutive Days'] = group['Time'].dt.date.diff().eq(timedelta(days=1)).cumsum().fillna(0)
        consecutive_days = group[group['Consecutive Days'] == 6]['Time'].dt.date.tolist()
        if len(consecutive_days) > 0:
            consecutive_days_result.append((name, consecutive_days))

    # Condition (b): Employees with less than 10 hours between shifts but greater than 1 hour
    time_between_shifts_result = []
    for name, group in data.groupby('Employee Name'):
        group['Time Difference'] = group['Time'].shift(-1) - group['Time Out']
        valid_shifts = group[(group['Time Difference'] > timedelta(hours=1)) & (group['Time Difference'] < timedelta(hours=10))]
        if not valid_shifts.empty:
            time_between_shifts_result.append((name, valid_shifts['Time'].tolist(), valid_shifts['Time Out'].tolist()))

    # Condition (c): Employees who have worked for more than 14 hours in a single shift
    long_single_shift_result = []
    for name, group in data.groupby('Employee Name'):
        long_shifts = group[group.apply(lambda x: calculate_hours_difference(x['Time'], x['Time Out']) > 14, axis=1)]
        if not long_shifts.empty:
            long_single_shift_result.append((name, long_shifts['Time'].tolist(), long_shifts['Time Out'].tolist()))

    return consecutive_days_result, time_between_shifts_result, long_single_shift_result

# path of the excel file to be read
excel_file_path = './Assignment_Timecard.xlsx'

data = pd.read_excel(excel_file_path)

consecutive_days, time_between_shifts, long_single_shift = analyze_employee_data(data)

# Print the results
print("Employees who have worked for 7 consecutive days:")
for result in consecutive_days:
    print(result)

print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
for result in time_between_shifts:
    print(result)

print("\nEmployees who have worked for more than 14 hours in a single shift:")
for result in long_single_shift:
    print(result)
