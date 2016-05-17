
import pyPdf
import argparse
import sqlite3
import os.path

from urlparse import urlparse
from collections import Counter

import config
import database_creation


def create_signature(filename):
    """ current idea - most frequent url """

    PDFFile = open(filename,'rb')


    PDF = pyPdf.PdfFileReader(PDFFile)
    pages = PDF.getNumPages()
    key = '/Annots'
    uri = '/URI'
    ank = '/A'

    urls = []
    for page in range(pages):

        pageSliced = PDF.getPage(page)
        pageObject = pageSliced.getObject()

        if pageObject.has_key(key):
            ann = pageObject[key]
            for a in ann:
                u = a.getObject()
                if u[ank].has_key(uri):
                    urls.append(u[ank][uri])

    urls = [urlparse(url).netloc for url in urls]
    most_frequent_url = Counter(urls).most_common()[0][0]

    return most_frequent_url 


def database_check(signature):
    if not os.path.exists(config.DATABASE):
        database_creation.create_database()

    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM %s WHERE %s=?' % (config.TABLENAME, config.SIGN_COLUMN), (signature,))
     
    if not c.fetchone():
        c.execute('INSERT INTO %s VALUES (?)' % config.TABLENAME, (signature,))
        conn.commit()
        c.close()
        return False
    else:
        return True
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    try:
        signature = create_signature(args.filename)
    except IOError as e:
        print e

    if database_check(signature)
        print signature, 'already in database'
    else:
        print signature, 'added in database'


if __name__ == '__main__':
    main()
