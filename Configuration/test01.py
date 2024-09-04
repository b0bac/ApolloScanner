import datetime
import chinese_calendar
def init_year():
    today = datetime.date.today()
    year = str(today).split("-")[0]
    print(year)
    start_date = datetime.datetime(int(year), 1, 1)
    end_date = datetime.datetime(int(year), 12, 31)
    print(start_date)
    print(end_date)
    '''
    try:
        result = DutyTable.objects.filter(date__range=(start_date,end_date))
    except Exception as reason:
        print(reason)
    print("b")
    count = result.count()
    print(count)
    if count > 0:
        return 
    '''
    current = start_date
    translate_dictionary: dict = {
	"New Year's Day": "1",
	"Spring Festival": "2",
	"Tomb-sweeping Day": "3",
	"Labour Day": "4",
	"Dragon Boat Festival": "5",
	"Mid-autumn Festival": "6",
	"National Day": "7"
    }
    print("Begin")
    while current < end_date:
        print(current)
        detail = chinese_calendar.get_holiday_detail(current)
        print(detail)
        overtime_string = detail[1] if detail[1] is not None else "0"
        print("overtime:" + overtime_string)
        work_type = "1" if detail[1] is not None else "0"
        print("work_type:" + work_type)
        day = {
            "date": current,
            "weekday": str(current.weekday()),
            "overtime_type": overtime_string,
            "work_type": work_type
        }
        print(day)
        #DutyTable.objects.create(**day)
        print("GoGoGo")
        current += datetime.timedelta(days=1)
        print("OK")

init_year()
