import gspread
from datetime import datetime, date, time

credential = gspread.service_account("budget-credentials.json")
categories = [['Зарплата','Стипа','Халтурка','Долг','Подарок','Матпомощь','ХЗ'], ['Еда','Хозяйство','Абонентка','Медицина','Поездки','Электроника','Шмот',          'Расходники','Долг','Ignis','Fun','Подарки','Донат','Х3']]
usernames = {'MayHatten': 'Соня', 'battlekruiser' : 'Саня'}

url = "https://docs.google.com/spreadsheets/d/1LIljx0OIq4LguS7L2jwxuev-uIMtWCsQrOvEPx4pun8/edit#gid=1532825902"
sheet = credential.open_by_url(url)

def get_row_number(sheet):
    values = sheet.get_all_values()
    for i,val in enumerate(values):
        if len(val[0])==0:
            return i
    return len(values)

def add_record(sheet,id_,obj,sum_,cat,user,place=None):
    inp = sheet.get_worksheet(id_)
    row_number = get_row_number(inp)+1 #TODO: dont count this every time you bitch
    cur_date = datetime.now().timetuple()
    year = cur_date[0]
    month = cur_date[1]
    day = cur_date[2]
    str_data = '%d.%d.%d' %(day,month,year)
    if cat not in categories[id_]:
        cat = categories[id_][-1]
    #if user not in usernames:
    #    user = usernames['MayHatten']
    record = [str_data,day,month,year,obj,sum_,cat,user]
    if id_==1 and place:
        record.append(place)
    inp.update('A%d'%(row_number),[record])