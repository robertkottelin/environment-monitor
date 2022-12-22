import psycopg2
from configparser import ConfigParser


def config_database(filename='/home/piro/PROJECTS/environment-monitor/backend/database.ini', section='postgresql'):
    '''
    Read the database configuration from the specified INI file and section.
    Return the configuration as a dictionary.
    '''
    # Create a parser to read the INI file
    parser = ConfigParser()

    # Read the INI file
    parser.read(filename)

    # Get the specified section, defaulting to 'postgresql'
    db = {}
    if parser.has_section(section):
        # Get the parameters from the section
        params = parser.items(section)
        # Add the parameters to the dictionary
        for param in params:
            db[param[0]] = param[1]
    else:
        # Raise an exception if the section is not found
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    # Return the dictionary with the configuration
    return db


def connect():
    '''
    Connect to the PostgreSQL database server and create a cursor.
    Return the connection and cursor objects.
    '''
    conn = None
    try:
        # Read the database configuration
        params = config_database()

        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # Create a cursor
        cur = conn.cursor()

        # Execute a statement to get the database version
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # Display the database server version
        db_version = cur.fetchone()
        print('Connection successful!')

        # Return the connection and cursor objects
        return conn, cur

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_temperature(conn, cur, temperature):
    '''
    Insert a temperature reading into the 'temperatures' table in the database.
    '''
    # Create the INSERT query
    postgres_insert_query = """
        INSERT INTO temperatures (celsius, created_at)
        VALUES (%s, NOW())
    """

    # Execute the INSERT query with the temperature reading
    record_to_insert = ([temperature])
    cur.execute(postgres_insert_query, record_to_insert)

    # Commit the changes to the database
    conn.commit()
    # cur.close()
    # conn.close()
