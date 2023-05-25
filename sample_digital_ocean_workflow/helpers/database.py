import psycopg2
from psycopg2.extensions import AsIs
import config

def db_connect():
	db_cred = config.do_cred
	user = config.do_user
	password = config.do_password
	host = config.do_host
	port = config.do_port
	database = config.do_database
	connection = psycopg2.connect(user=user,password=password,host=host,port=port,database=database)
	return(connection)

def getpagedetails(url):
    try:
        connection = db_connect()
        cursor = connection.cursor()
        connection.autocommit = True
        sql = """select pageid,domainid from pages where pageurl = %s"""
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            return({'pid':result[0],'did':result[1]})
        else:
        	return(False)
    except (Exception) as error:
        return(error)
    finally:
        cursor.close()
        connection.close()