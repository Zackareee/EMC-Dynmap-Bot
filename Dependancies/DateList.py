from datetime import date, timedelta
import os
if os.name == 'nt':
    s = "#"
else:
    s = "-"
def month_date(start_date):
    end_date = start_date + + timedelta(days=14)
    if end_date > date.today():
        end_date = date.today() + timedelta(days=1)

    for n in range(int ((end_date - start_date).days)):
        yield (start_date + timedelta(n)).strftime(f'%{s}d.%{s}m.%y')
