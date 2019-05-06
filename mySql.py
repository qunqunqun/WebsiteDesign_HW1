#此文件利用SQL接口进行操作
import pymysql

class Mysql:

    def test(self,user_name,password):
        conn = pymysql.connect(host="localhost", user="root", password="beibei", db="flask")
        cur = conn.cursor()
        sql = "select * from customes \
                    where Name = '%s' and Password = '%s' " % (user_name, password)
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        cur.close()
        conn.close()

        if len(result) == 0:
            return False
        else:
            return True

    def insert(self,user_name,password,email):
        conn = pymysql.connect(host="localhost", user="root", password="beibei", db="flask")
        cur = conn.cursor()
        sql = "select * from customes \
                            where Name = '%s' and Password = '%s' " % (user_name, password)
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) == 1:
            return False
        sql = 'insert into customes values("%s","%s","%s")'% (user_name, password,email)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        return True

    def FindMyThing(self,name): #根据名字找到卖的物品
        conn = pymysql.connect(host="localhost", user="root", password="beibei", db="flask")
        cur = conn.cursor()
        sql = "select * from things where NAME = '%s'" %(name)
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def CheckInsert(self,Name,T_name,T_des,T_img): #检查名字
        #查看是否是合法的，已经有这个物品存在
        conn = pymysql.connect(host="localhost", user="root", password="beibei", db="flask")
        cur = conn.cursor()
        sql = "select * from things where NAME = '%s' and T_name = '%s'" % (Name,T_name)
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) > 0: #已经存在，不合法
            return False
        #否则插入并且返回
        sql = 'insert into things values("%s","%s","%s","%s")' % (Name, T_name, T_des,Name +'_'+T_name+".jpg")
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return True

    def deFromDB(self,name,T_name): #执行删除操作
        #首先查询有无
        conn = pymysql.connect(host="localhost", user="root", password="beibei", db="flask")
        cur = conn.cursor()
        sql = "select * from things where NAME = '%s' and T_name = '%s'" % (name, T_name)
        cur.execute(sql)
        result = cur.fetchall()
        # 无则返回
        if len(result) == 0:
            return False
        #有则删除
        sql = "delete FROM things where NAME = '%s' and T_name = '%s'" % (name, T_name)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return True