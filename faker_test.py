from faker import Faker

from mysql_helper import get_connection, get_cursor

fak = Faker('zh_CN')
con = get_connection()
cursor = get_cursor(con)


# use ishop;
# create table tb_sales(
# id int(20) primary key auto_increment ,
# Quantity int(22),
# UnitPrice int(100),
# CustomerID int(128),
# time1 date not null
# )

def main():
    sql = 'insert into tb_sales(Quantity,UnitPrice,CustomerID,time1) values (%s,%s,%s,%s) '
    for i in range(10000):
        print(i)
        # date_between()：随机生成指定范围内日期，参数：start_date，end_date
        # time1 = fak.date_between(start_date='2017-1-1',end_date='-750d')
        time1 = fak.date_between(start_date='-4y', end_date='now')
        # 数量
        Quantity =fak.random_int(min=5,max=99)
        # 单价
        UnitPrice = fak.random_int(min=48,max=2000)
        # 客户id
        CustomerID = fak.random_number(5,True)

        print(time1,Quantity,UnitPrice,CustomerID)
        # cursor.execute(sql,(time1,Quantity,UnitPrice,CustomerID))
        # con.commit()
