import gdoc
import matplotlib.pyplot as plt
import numpy as np
import string


sheet = gdoc.sheet
stat_sheet = sheet.get_worksheet(2)
titles = stat_sheet.row_values(2)
income_x = titles.index('Доход')
spend_x = titles.index('Расход')
res_x = titles.index('Остаток')
cats = stat_sheet.row_values(3)
categories = [[],[]]
categories[0]=cats[income_x:spend_x-1]
categories[1]=cats[spend_x:res_x-1]


def get_cell_letters(num):
    upper = list(string.ascii_uppercase)
    letters = upper.copy()
    n = num//len(upper)
    for i in range(n):
        for j in range(len(upper)):
            letters.append(upper[i]+upper[j])
    return letters
letters = get_cell_letters(100)
start_letter = letters[income_x]
end_letter = letters[res_x]


start_month=5
start_year=2023
start_cell=4
def get_month_cell(month,year):
    return start_cell+(year-start_year)*12+month-start_month


def get_stats_month(user_id,month,year):
    stat_sheet = sheet.get_worksheet(2+user_id) #gdoc sheets 2 and 3 are stats 
    row=get_month_cell(month,year)
    if row<start_cell:
        return 'baka'
    data = stat_sheet.row_values(row)
    income_data = np.array([float(x.replace(',', '.')) for x in data[income_x:spend_x-1]])
    spend_data = np.array([float(x.replace(',', '.')) for x in data[spend_x:res_x-1]])
    income_sum = income_data.sum()
    spend_sum = spend_data.sum()
    res = float(data[res_x].replace(',','.'))
    plot_chart(income_data,categories[0],'Income') 
    plot_chart(spend_data,categories[1],'Spend')    
    return 'Stats for month %d year %d. Income %d. Outcome %d. Balance %d' %(month,year,int(income_sum),int(spend_sum),int(res))


def get_stats_year(user_id,year):
    stat_sheet = sheet.get_worksheet(2+user_id)
    if year<start_year:
        return 'baka'
    end_row = get_month_cell(12,year)
    if year == start_year:
        start_row = start_cell
    else:
        start_row = get_month_cell(1,year)
    str_ = "%s%d:%s%d"%(start_letter,start_row,end_letter,end_row)
    data = stat_sheet.get(str_)
    income_end = spend_x-income_x-1
    spend_end = res_x-income_x-1
    income_data = np.zeros(len(categories[0]))
    spend_data = np.zeros(len(categories[1]))
    for row in data:
        income_data+=np.array([float(x.replace(',', '.')) for x in row[:income_end]])
        spend_data+=np.array([float(x.replace(',', '.')) for x in row[income_end+1:spend_end]])
    income_sum = income_data.sum()
    spend_sum = spend_data.sum()
    res = float(data[-1][-1].replace(',','.'))
    plot_chart(income_data,categories[0],'Income') 
    plot_chart(spend_data,categories[1],'Spend')
    
    return 'Stats for year %d. Income %d. Outcome %d. Balance %d' %(year,int(income_sum),int(spend_sum),int(res))


def plot_chart(data,labels,title):
    fig, ax = plt.subplots()
    nz_data = data[data>0]
    nz_labels = np.array(labels)[data>0]
    sorted_idx = np.argsort(nz_data)
    ax.pie(nz_data[sorted_idx], labels=nz_labels[sorted_idx],autopct='%1.1f%%')
    ax.set_title(title)
    plt.savefig(title+'.png')