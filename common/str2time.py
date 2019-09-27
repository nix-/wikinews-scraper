#!/usr/bin/python
import time
import re


def str2time(str_time):
    s_time = re.split("[^a-zA-Z\d]+", str_time)

    a_time = time.time()

    if len(s_time) > 2:
        if len(s_time) <= 3:
            t_time = '1 '
            t_time += s_time[1] + ' '
            t_time += s_time[2]
        else:
            t_time = s_time[2] + ' '
            t_time += s_time[1] + ' '
            t_time += s_time[3]

        print(t_time)

        try:
            a_time = time.strptime(t_time, "%b %d %Y")
        except ValueError:
            try:
                a_time = time.strptime(t_time, "%d %b %Y")
            except ValueError:
                try:
                    a_time = time.strptime(t_time, "%B %d %Y")
                except ValueError:
                    try:
                        a_time = time.strptime(t_time, "%d %B %Y")
                    except ValueError:
                        print('Can not parse the format')

    return a_time
