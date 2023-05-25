import psycopg2
import config
from psycopg2.extensions import AsIs

def db_connect():
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
        sql = """select p.pageid,p.domainid,o.orgid from pages p left join domainorgrelation o on o.domainid = p.domainid where pageurl = %s"""
        cursor.execute(sql,[url])
        result = cursor.fetchall()
        if result:
            return({'pid':result[0][0],'did':result[0][1],'orgid':result[0][2]})
        else:
        	return(False)
    except (Exception) as error:
        return(error)
    finally:
        cursor.close()
        connection.close()

def getkeywords():
    try:
        connection = db_connect()
        cursor = connection.cursor()
        connection.autocommit = True
        sql = """select solution from solutions"""
        cursor.execute(sql)
        result = cursor.fetchall()
        return([item[0] for item in result])
    except (Exception) as error:
        return(error)
    finally:
        cursor.close()
        connection.close()


