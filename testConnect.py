import cx_Oracle

if __name__ == '__main__':
    db = cx_Oracle.connect('tduser01', 'td111222', '192.168.68.62:1521/tddb')
    curs = db.cursor()
    print('数据库连接成功')
    sqlStr = 'select * from test'
    curs.execute(sqlStr)
    arr = curs.fetchall()
    curs.close()
    db.close()
