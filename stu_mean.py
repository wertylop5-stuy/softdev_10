import sqlite3
from utils import sql
from utils.sql import *



db = sqlite3.connect("lol.db")
c = db.cursor()

def get_grades(c, student_name):
	val = c.execute("SELECT id FROM peeps WHERE name='%s'"%(student_name))
	
	id = -1
	for v in val:
		id = v
	
	courses = c.execute("SELECT code, mark FROM courses WHERE id=%d;"%(id))
	
	ret = {}
	for course in courses:
		ret[course[0]] = course[1]
	
	return ret

def get_average(c, student_name):
	courses = get_grades(c, student_name)
	
	avg = 0
	for grade in courses.values():
		avg += grade

	avg /= len(courses.keys())
	print avg


val = c.execute("SELECT peeps.id, mark FROM peeps, courses WHERE peeps.id = courses.id;")
for row in val:
	print row

get_grades(c, "bassnectar")
get_average(c, "bassnectar")

db.commit()
db.close()
