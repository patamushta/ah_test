import sqlite3
import os.path

import config


def create_database():
    if os.path.exists(config.DATABASE):
        print 'database already exists'
    else:
        conn = sqlite3.connect(config.DATABASE)
        conn.execute('create table %s (%s text)' % (config.TABLENAME, config.SIGN_COLUMN))
        conn.commit()
        conn.close()
        print 'database created'


if __name__ == '__main__':
    create_database()
    
