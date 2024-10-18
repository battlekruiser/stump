import gspread
#import stats
from datetime import datetime, date, time

credential = gspread.service_account("budget-credentials.json")
#categories = [['Зарплата','Стипа','Халтурка','Долг','Подарок','Матпомощь','ХЗ'],
#              ['Еда','Хозяйство','Абонентка','Медицина','Поездки','Электроника','Шмот/Косметика','Расходники','Долг','Ignis','Fun','Подарки','Донат','Х3']]



url = "https://docs.google.com/spreadsheets/d/1LIljx0OIq4LguS7L2jwxuev-uIMtWCsQrOvEPx4pun8/edit"
sheet = credential.open_by_url(url)

def get_categories():
    categories = [[],[]]
    stat_sheet = sheet.get_worksheet(2)
    titles = stat_sheet.row_values(2)
    income_x = titles.index('Доход')
    spend_x = titles.index('Расход')
    res_x = titles.index('Остаток')
    cats = stat_sheet.row_values(3)
    categories[0]=cats[income_x:spend_x-1]
    categories[1]=cats[spend_x:res_x-1]
    return categories

categories = get_categories()

usernames = {'MayHatten': 'Соня', 'battlekruiser' : 'Саня'}
userids   = {'MayHatten': 0,      'battlekruiser' : 1}

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
    print(str_data)
    if cat not in categories[id_]:
        cat = categories[id_][-1]
    #if user not in usernames:
    #    user = usernames['MayHatten']
    record = [day,month,year,obj,sum_,cat,user]
    if id_==1 and place:
        record.append(place)
    inp.update('A%d'%(row_number),str_data,raw=False) #https://docs.gspread.org/en/v5.12.0/api/models/worksheet.html#gspread.worksheet.Worksheet.update
    inp.update('B%d'%(row_number),[record])