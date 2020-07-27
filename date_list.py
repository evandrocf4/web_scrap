import datetime

start_date = datetime.date(2020,3,17)
end_date = datetime.date.today()
timedelta = end_date - start_date

date_list = [str(end_date - datetime.timedelta(days=x)) for x in range(0, timedelta.days)]
