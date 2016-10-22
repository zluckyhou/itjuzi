#投资事件分析

invest_event = read.csv('C:\\Users\\zluck\\Documents\\统计\\IT橘子投资事件分析\\invest_event.csv',header = TRUE,as.is = T)
head(invest_event)

# 中国市场上最活跃的投资方都有哪些
investor = invest_event$investor
inv = NULL
for (i in investor){
  inv = c(inv,strsplit(i,',')[[1]])
}

inv_freq = as.data.frame(sort(table(inv),decreasing = T)[-1])
head(inv_freq,11)
barplot(sort(table(inv),decreasing = T)[2:11],col = 'red')

# 腾讯作为投资方竟然排在第7，我们看一下腾讯的投资都有哪些，第一笔投资时什么时候
inv_tx = invest_event %>% filter(investor == '腾讯')
inv_tx[1,]
inv_tx[dim(inv_tx)[1],]

#排名前10的创业首选地方
loc = invest_event %>% group_by(place) %>% summarise(cnt = n()) %>% arrange(desc(cnt)) %>% head(10)
loc
barplot(sort(table(invest_event$place),decreasing = T)[1:10],col = 'orange')

# 哪些创业企业获得了成功
invest_event %>% group_by(company) %>% summarise(cnt = n()) %>% arrange(desc(cnt))
# 获得投资次数最多的20家公司
sus_cp = invest_event %>% group_by(company) %>% summarise(cnt = n()) %>% arrange(desc(cnt)) %>% head(20)

