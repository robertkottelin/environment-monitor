import psycopg2
from configparser import ConfigParser


def config_database(filename='/home/piro/PROJECTS/environment-monitor/backend/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db
  
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config_database()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        #print(db_version)
        print('Connection successful!')

        return conn, cur

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_temperature(conn, cur, temperature):
    postgres_insert_query = """
        INSERT INTO temperatures (celsius, created_at)
        VALUES (%s, NOW())
    """
    record_to_insert = ([temperature])
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    # cur.close()
    # conn.close()