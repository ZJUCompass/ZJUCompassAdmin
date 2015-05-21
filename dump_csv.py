#-*- encoding:utf-8 -*-
import sys,os
import sqlite3
reload(sys)
sys.setdefaultencoding("utf-8")

def dump_info(dst_file,table="teacher",department=""):
    if table == "teacher":
        f = open(dst_file,"w")
        f.write("teacher_id\tname\tdepartment\ttitle\tphone\temail\tbuilding\troom\tresearch\n")
        db = sqlite3.connect("data/zjucompass.db")
        sqlcmd = "select * from teacher_info where 1=1"
        if department != "":
            sqlcmd += " and department='" + department + "'"
        print sqlcmd
        
        cur = db.execute(sqlcmd)
        row_count = 0
        for row in cur.fetchall():
            terms = []
            for t in row:
                if not str(t).strip():
                    terms.append("null")
                else:
                    terms.append(str(t).strip())
            f.write("\t".join(terms)+"\n")
            row_count += 1
        print str(row_count) + " rows are found and written."
        f.close()
    elif table == "matter":
        f = open(dst_file,"w")
        f.write("事项名称\t事项编号（或序号）\t服务类别\t办件类型\t实施主体\t办事依据\t申请材料\t办事流程描述\t办事流程图\t承诺期限\t收费依据\t收费金额\t表格下载\t受理机构\t受理时间\t受理地址\t岗位（或责任人）\t咨询电话\t监督电话\t详情链接\n")
        db = sqlite3.connect("data/zjucompass.db")
        sqlcmd = "select * from matter_info where 1=1"
        print sqlcmd
        
        cur = db.execute(sqlcmd)
        row_count = 0
        for row in cur.fetchall():
            terms = []
            for t in row:
                if not str(t).strip():
                    terms.append("无")
                else:
                    terms.append(str(t).strip())
            f.write("\t".join(terms)+"\n")
            row_count += 1
        print str(row_count) + " rows are found and written."
        f.close()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        filename = sys.argv[1]
        table = sys.argv[2]
        if table not in ["teacher","matter"]:
            print "ERROR:table must be teacher or matter."
            sys.exit(0)
        department = ""
    elif len(sys.argv) == 4:
        filename = sys.argv[1]
        table = sys.argv[2]
        if table not in ["teacher","matter"]:
            print "ERROR:table must be teacher or matter."
            sys.exit(0)
        department = sys.argv[3]
    else:
        print "Usage:<filename> <table> <department:optional>"
        sys.exit(0)

    dump_info(filename,table,department)
