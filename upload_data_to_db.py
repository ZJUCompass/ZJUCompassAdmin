# -*- coding:utf-8 -*-

import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")
from collections import defaultdict
import sqlite3

def load_teacher_info(filename):
    teacher_info_dict = defaultdict(lambda : defaultdict(lambda:"null"))
    for line in open(filename,"r").readlines():
        if not line.strip():
            continue
        terms = line.split("\t")
        if len(terms) != 9:
            continue
        teacher_id = terms[0]
        if not teacher_id.strip():
            continue
        teacher_info_dict[teacher_id]["teacher_name"] = terms[1]
        teacher_info_dict[teacher_id]["teacher_department"] = "计算机学院"
        teacher_info_dict[teacher_id]["teacher_title"] = terms[3]
        teacher_info_dict[teacher_id]["teacher_phone"] = terms[4]
        teacher_info_dict[teacher_id]["teacher_email"] = terms[5]
        teacher_info_dict[teacher_id]["teacher_building"] = terms[6]
        teacher_info_dict[teacher_id]["teacher_room"] = terms[7]
        teacher_info_dict[teacher_id]["teacher_field"] = terms[8]

    return teacher_info_dict

def load_all_teacher_info(filename,teacher_info_dict):
    for line in open(filename,"r").readlines():
        if not line.strip():
            continue
        terms = line.split("\t")
        if len(terms) != 9:
            continue
        teacher_id = terms[0]
        if not teacher_id.strip():
            continue
        if teacher_id not in teacher_info_dict:
            teacher_info_dict[teacher_id]["teacher_name"] = terms[1]
            teacher_info_dict[teacher_id]["teacher_department"] = terms[2]
            teacher_info_dict[teacher_id]["teacher_title"] = terms[3]
            teacher_info_dict[teacher_id]["teacher_phone"] = terms[4]
            teacher_info_dict[teacher_id]["teacher_email"] = terms[5]
            teacher_info_dict[teacher_id]["teacher_building"] = terms[6]
            teacher_info_dict[teacher_id]["teacher_room"] = terms[7]
            teacher_info_dict[teacher_id]["teacher_field"] = terms[8]

def create_teacher_table():
    conn = sqlite3.connect("data/zjucompass.db")
    
    conn.execute(""" CREATE TABLE teacher_info
                (teacher_id integer primary key autoincrement,
                 name varchar(50),
                 department varchar(100),
                 title varchar(50),
                 phone varchar(100),
                 email varchar(100),
                 building varchar(255),
                 room varchar(100),
                 field text);""")
    conn.commit()
    conn.close()

def create_matter_table():
    conn = sqlite3.connect("data/zjucompass.db")
    
    conn.execute(""" CREATE TABLE matter_info
                (   matter_name varchar(50),
                    matter_id varchar(20) primary key,
                    service_type varchar(50),
                    matter_type varchar(50),
                    matter_executor varchar(50),
                    matter_basis varchar(50),
                    matter_meterial varchar(500),
                    matter_description varchar(500),
                    matter_graph varchar(50),
                    matter_promise_date varchar(50),
                    matter_fee_depends varchar(50),
                    matter_fee_amount varchar(50),
                    matter_graph_download varchar(50),
                    matter_agent varchar(50),
                    matter_time varchar(50),
                    matter_address varchar(50),
                    matter_officer varchar(50),
                    matter_consult_phone varchar(50),
                    matter_complaint_phone varchar(50),
                    matter_detail_url varchar(100));""")
    conn.commit()
    conn.close()


def load_matter_info(filename,matter_info_dict):
    for line in open(filename,"r").readlines():
        if not line.strip():
            continue
        terms = line.split("\t")
        if len(terms) != 20:
            continue
        matter_id = terms[1]
        if matter_id not in matter_info_dict:
            matter_info_dict[matter_id]["matter_name"] = terms[0]
            matter_info_dict[matter_id]["service_type"] = terms[2]
            matter_info_dict[matter_id]["matter_type"] = terms[3]
            matter_info_dict[matter_id]["matter_executor"] = terms[4]
            matter_info_dict[matter_id]["matter_basis"] = terms[5]
            matter_info_dict[matter_id]["matter_meterial"] = terms[6]
            matter_info_dict[matter_id]["matter_description"] = terms[7]
            matter_info_dict[matter_id]["matter_graph"] = terms[8]
            matter_info_dict[matter_id]["matter_promise_date"] = terms[9]
            matter_info_dict[matter_id]["matter_fee_depends"] = terms[10]
            matter_info_dict[matter_id]["matter_fee_amount"] = terms[11]
            matter_info_dict[matter_id]["matter_graph_download"] = terms[12]
            matter_info_dict[matter_id]["matter_agent"] = terms[13]
            matter_info_dict[matter_id]["matter_time"] = terms[14]
            matter_info_dict[matter_id]["matter_address"] = terms[15]
            matter_info_dict[matter_id]["matter_officer"] = terms[16]
            matter_info_dict[matter_id]["matter_consult_phone"] = terms[17]
            matter_info_dict[matter_id]["matter_complaint_phone"] = terms[18]
            matter_info_dict[matter_id]["matter_detail_url"] = terms[19]



def insert_teacher_info(teacher_info_dict):

    conn = sqlite3.connect("data/zjucompass.db")

    for t_id in teacher_info_dict:
        sqlcmd = "INSERT INTO teacher_info(teacher_id,name,department,title,phone,email,building,room,field) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(t_id,teacher_info_dict[t_id]["teacher_name"],teacher_info_dict[t_id]["teacher_department"],teacher_info_dict[t_id]["teacher_title"],teacher_info_dict[t_id]["teacher_phone"],teacher_info_dict[t_id]["teacher_email"],teacher_info_dict[t_id]["teacher_building"],teacher_info_dict[t_id]["teacher_room"],teacher_info_dict[t_id]["teacher_field"])
        print sqlcmd
        conn.execute(sqlcmd)
    conn.commit()
    conn.close()


def insert_matter_info(matter_info_dict):

    conn = sqlite3.connect("data/zjucompass.db")
    matter_ids = set()
    for m_id in matter_info_dict:
        sqlcmd = "INSERT INTO matter_info(matter_id,matter_name,service_type,matter_type,matter_executor,matter_basis,matter_meterial,matter_description,matter_graph,matter_promise_date,matter_fee_depends,matter_fee_amount,matter_graph_download,matter_agent,matter_time,matter_address,matter_officer,matter_consult_phone,matter_complaint_phone,matter_detail_url) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(m_id,matter_info_dict[m_id]["matter_name"],matter_info_dict[m_id]["service_type"],matter_info_dict[m_id]["matter_type"],matter_info_dict[m_id]["matter_executor"],matter_info_dict[m_id]["matter_basis"],matter_info_dict[m_id]["matter_meterial"],matter_info_dict[m_id]["matter_description"],matter_info_dict[m_id]["matter_graph"],matter_info_dict[m_id]["matter_promise_date"],matter_info_dict[m_id]["matter_fee_depends"],matter_info_dict[m_id]["matter_fee_amount"],matter_info_dict[m_id]["matter_graph_download"],matter_info_dict[m_id]["matter_agent"],matter_info_dict[m_id]["matter_time"],matter_info_dict[m_id]["matter_address"],matter_info_dict[m_id]["matter_officer"],matter_info_dict[m_id]["matter_consult_phone"],matter_info_dict[m_id]["matter_complaint_phone"],matter_info_dict[m_id]["matter_detail_url"])
        print sqlcmd
        if m_id not in matter_ids:
            try:
                conn.execute(sqlcmd)
            except:
                pass
            matter_ids.add(m_id)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    '''
    create_teacher_table()
    teacher_info_dict = load_teacher_info("data/teacher_info.csv")
    #teacher_info_dict = {}
    load_all_teacher_info("data/finally_teacher_info.txt", teacher_info_dict)
    #for t_id in teacher_info_dict:
    #    print teacher_info_dict[t_id]["teacher_field"]
    insert_teacher_info(teacher_info_dict)
    '''
    #create_matter_table()
    matter_info_dict = defaultdict(lambda : defaultdict(lambda:"null"))
    load_matter_info("data/matter_info.csv",matter_info_dict)
    for matter_id in matter_info_dict:
        print matter_info_dict[matter_id]['matter_name']
    insert_matter_info(matter_info_dict)

