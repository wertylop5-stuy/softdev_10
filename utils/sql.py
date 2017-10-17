import csv


SQL_TYPE_DICT = {
	type(""): "STRING",
	type(0): "INTEGER",
	type(7.8): "REAL"
}

def create_type_tuple(list):
	'''
	Returns a tuple containing the corresponding SQL type for
	each element in the list
	'''
	
	res = []
	
	for value in list:
		res.append(SQL_TYPE_DICT[type(value)])
	return tuple(res)
		

def create_value_string(list):
	'''
	Pass in a list of values. This function will format
	it to be used with the INSERT INTO SQL commmand
	
	Returns a string that can be used in the SQL command
	'''
	
	values = "("
	for value in list:
		values += '"' + value + '"'
		values += ", "
	
	if len(values) > 1:	
		values = values[:len(values)-2]
	
	return values + ")"

def sql_insert_into(table_name, fields, record):
	'''
	fields and record should be strings. Use the create_value_string
	function to format the values before using this function
	
	Returns a SQL command in the form of a string
	'''
	
	return "INSERT INTO " + table_name + " " + fields + \
		" VALUES " + record + ";"

def populate_table(csv_file, table_name, cursor):
	'''
	Uses the provided cursor to a database and populates the 
	table in the given database with data from the csv file
	
	csv_file: string
	table_name: string
	cursor: object
	'''
	
	with open(csv_file) as file:
		reader = csv.DictReader(file)
		
		for row in reader:
			'''
			apparently keys() will always be in the same order
			provided that the dict wasn't modified in between
			calls
			'''
			
			cursor.execute(
				sql_insert_into(table_name,
					create_value_string(row.keys()),
					create_value_string(
						[row[key] for key in row.keys()])
				)
			)
	




