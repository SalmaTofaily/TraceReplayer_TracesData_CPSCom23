def sec_to_min_display(s):
    time_display = str(int(float(s)/60)) + ' min'
    remaining_Seconds = float(s) % 60

    if remaining_Seconds != 0:
        time_display = time_display + ' ' + str(int(remaining_Seconds))+' sec'
    return time_display