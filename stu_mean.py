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
	return avg


classes = formatted_select(c, ["name", "code", "mark"],
	["courses", "peeps"], "peeps.id = courses.id")

for v in classes:
	print "name: %s, code: %s, mark: %d"%(v["name"], v["code"], v["mark"])

students = formatted_select(c, ["name", "id"], ["peeps"], "")
students_and_avg = {}
for student in students:
	students_and_avg[student["id"]] = get_average(c, student["name"])

print students_and_avg

try:
	c.execute("CREATE TABLE peeps_avg (id INTEGER PRIMARY KEY, average REAL);")
	for key in students_and_avg.keys():
		c.execute(
			sql_insert_into("peeps_avg",
				create_value_string(["id", "average"]), 
				create_value_string([key, students_and_avg[key]]))
		)
except sqlite3.OperationalError:
	pass

c.execute(sql_update("peeps_avg", "average", 25, "id=5"))


db.commit()
db.close()
