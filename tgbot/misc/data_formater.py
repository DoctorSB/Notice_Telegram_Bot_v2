import datetime
import re


def date_formater(str):
    date = re.split(r'\s', str)
    if len(date) == 1:
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        date.append(month)
        date.append(year)
        date.append(12)
        date.append(0)
    if len(date) == 2:
        year = datetime.datetime.now().year
        date.append(year)
        date.append(12)
        date.append(0)
    if len(date) == 3:
        date.append(12)
        date.append(0)
    if len(date) == 4:
        date.append(0)
    if len(date) > 5:
        return datetime.datetime.now()
    date = [int(i) for i in date]
    date = datetime.datetime(date[2], date[1], date[0], date[3], date[4])
    return date


if __name__ == '__main__':
    print(date_formater('12 12 2021 12 12'))
    print(date_formater('1 3 2021'))
    print(date_formater('12 12 2021'))
    print(date_formater('12 12'))
    print(date_formater('12'))
