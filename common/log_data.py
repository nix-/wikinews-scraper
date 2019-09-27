#!/usr/bin/python


def log_append_data_into_file(file, data):

    f = open(file, "a")
    f.write(data)
    f.close()
    return


log_append_data_into_file('test.txt', 'test1 TEST2')