# coding = utf-8
import os
import pandas as pd
from pandas import Series,DataFrame
from dateutil.parser import parse
import pymysql


from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def merge_file(path):
    fls = os.listdir(path)
    ls_csv = [i for i in fls if os.path.splitext(i)[1] == '.csv']
    invest_ls = []
    for i in ls_csv:
        invest_ls.append(pd.read_csv(path+r'\\'+i,index_col=0,usecols=range(1,9),encoding='gb18030'))
    invest_info = pd.concat(invest_ls,axis=0)
    return invest_info
path = r'C:\Users\zluck\Documents\GitHub\itjuzi'
invest_info = merge_file(path)


#日期存在一些错误值，首先把这些错误值筛选出来，然后将错误日期解析为该日期的前一天

dates = []
for i in range(len(invest_info)):
    try:
        dates.append(parse(invest_info.index[i]))
    except Exception as e:
        print (invest_info.index[i])
        try:
            dates.append(parse(invest_info.index[i+1]))
            print (parse(invest_info.index[i+1]))
        except Exception as e:
            dates.append(parse(invest_info.index[i+2]))
            print (parse(invest_info.index[i+2]))

# 将索引修改为解析后的日期格式
invest_info.index = dates
invest_info.index.name = 'date'
invest_info.to_csv(path + '\\'+ 'invest_event.csv')

# 将投资事件信息存储到mysql中
conn = pymysql.connect(host = 'localhost',port = 3306,user = 'root',passwd = 'helloworld',db = 'python',charset = 'utf8')
cur = conn.cursor()
#mysql需要设置编码才能存储中文 ALTER DATABASE python CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
# 参见http://stackoverflow.com/questions/34305587/uploading-python-pandas-dataframe-to-mysql-internalerror-1366-incorrect-str
# 由于investor列的有些值长度比较长，而mysql默认为varchar(63)，所以还需要修改字段长度
# alter table invest_event modify investor varchar(255)
invest_info.to_sql(name = 'invest_event',con = conn,if_exists = 'replace',flavor = 'mysql',dtype = {'investor':'varchar(255)'})

invest_info = pd.read_csv(r'C:\Users\zluck\Documents\GitHub\itjuzi\invest_event.csv',encoding='gb18030')
# 最活跃的投资机构都有哪些
investors = []
for i in invest_info.investor:
    if pd.notnull(i):
        investors.extend(i.split(','))
    else:
        print (invest_info[invest_info.investor.isnull()])

active_investors = Series(investors).value_counts()

# 构造投资机构云图

ls = []
for i in zip(active_investors.index,active_investors.values):
    ls.append(i)

wc = WordCloud(font_path = r'C:\Windows\Fonts\simkai.ttf') #wordcloud默认字体为DroidSansMono,如果要支持中文，需要设置字体
wc.generate_from_frequencies(ls[1:]) # 投资方未透露的投资事件最多，所以去掉第一个

plt.imshow(wc)
plt.axis('off')
plt.show()

# 最早的一笔投资是什么时候
invest_info.iloc[-1,]


