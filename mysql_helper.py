import pymysql

# 获取数据库连接
def get_connection():
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = '123456'
    database = 'douban'
    con = pymysql.connect(host, user, password, database, charset='utf8mb4', port=port)
    return con

# 获取游标
def get_cursor(con):
    return con.cursor()

# 关闭连接
def close_connection(con):
    con.close()

# sql注入风险
def insert_movie(con,cursor,movie_dict):
    sql = 'insert into movie (title,actors,release,release_time,cover) values ("%s","%s","%s","%s","%s")' % (movie_dict['title'],movie_dict['stars'],movie_dict['releasetime'],movie_dict['photo'])
    print(sql)
    cursor.execute(sql)
    con.commit()

def insert_movie2(con,cursor,movie_dict):
    sql = 'insert into articles (title,img,content,source_l,time_l) values (%s,%s,%s,%s,%s)'
    print(sql)
    cursor.execute(sql,(movie_dict['title'],movie_dict['img'],movie_dict['content'],movie_dict['source'],movie_dict['time']))
    con.commit()
