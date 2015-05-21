#-*- encoding:utf-8 -*-
import sys,os
import sqlite3

if __name__ == "__main__":
    db = sqlite3.connect("data/zjucompass.db")
    for line in open("data/department_list.txt","r").readlines():
        terms = line.strip().split("\t")
        if len(terms) != 2:
            continue
        department = terms[0]
        name = terms[1]
        sqlcmd = "update teacher_info set department='%s' where name='%s'"%(department,name)
        #print sqlcmd
        db.execute(sqlcmd)
        db.commit()
    db.close()
