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
        sql = """select p.pageid,p.domainid,d1.orgid, string_agg(p2.pageurl, ', ') AS link_list FROM pages p left join domainorgrelation d1 on d1.domainid = p.domainid left join pagerelation pr on pr.startpage = p.pageid left join pages p2 on p2.pageid = pr.endpage left join domainorgrelation o2 on p2.domainid = o2.domainid left join domains d2 on d2.domainid = o2.domainid left join orgs or1 on or1.orgid = o2.orgid where p.pageurl = %s and (d2.orgrelationignore is False or d2.orgrelationignore is null) GROUP BY p.pageid,p.domainid,d1.orgid"""
        cursor.execute(sql,[url])
        result = cursor.fetchall()
        if result:
            return({'pid':result[0][0],'did':result[0][1],'orgid':result[0][2],'links':result[0][3].split(',')})
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

def get100randomcasestudies():
    try:
        connection = db_connect()
        cursor = connection.cursor()
        connection.autocommit = True
        sql = """select pageurl from pages, to_tsquery('english', 'case:* & stud:*') AS q where (pages.pagedescription is not NULL and tsv_pageurl @@ q) and pageurl not ilike '%443%' and language = 'en' order by random() limit 100"""
        cursor.execute(sql)
        result = cursor.fetchall()
        return([item[0] for item in result])
    except (Exception) as error:
        return(error)
    finally:
        cursor.close()
        connection.close()