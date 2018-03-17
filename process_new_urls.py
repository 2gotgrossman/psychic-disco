import sqlite3
import parse_urls
# for debugging purposes
import os, sys

blacklisted = [b'https://www.google.com/search',
               b'https://www.facebook.com',
               b'chrome://',
               b'https://www.youtube.com',
               b'https://mail.google.com',
               b'https://docs.google.com',
               b'file://'
              ]

# DATABASE
sqlite_file = 'history.sqlite'

# TABLES
to_process_urls_table = 'to_process_urls'
stored_urls_table = 'processed_urls'
raw_text_table = 'raw_text'
tokenized_text_table = 'tokenized_text'
blacklisted_table = 'blacklisted_urls'
titles_table     = 'titles'


# IDS AND COLUMNS
primary_key = 'url' 
processed_text = 'processed_text'
unprocessed_text = 'unprocessed_text'
title_column = 'title'



# TODO
def clean_url(url):
    pre_hash_url = url.split(b"#")[0]
    return pre_hash_url

def is_blacklisted(url, cursor):
    if url == b"":
        return True
    for bad in blacklisted:
        if bad in url:
            return True
    else:
        return False

def insert_into_table(cursor, table, url, col_name=None, value=None):
    if col_name and value:
        cursor.execute("INSERT OR IGNORE INTO {tn} ({idf}, {cn}) VALUES (?,?)".\
            format(tn=table, idf=primary_key, cn=col_name), (url, value))
    else:
        cursor.execute("INSERT OR IGNORE INTO {tn} ({idf}) VALUES (?)".\
            format(tn=table, idf=primary_key), (url,))

def delete_from_to_process_table(cursor, url):
    cursor.execute('DELETE FROM {tn} WHERE {pk}=(?)'.\
            format(tn=to_process_urls_table, pk=primary_key), (url,) )


def process_url(cleaned_url, original_url, cursor):
    """
        return: True if completed without error. False if errorful.
    """
    # 1. Parse URL
    # 2. Add to tables
    # 3. Add to processed_urls table
    # 4. Remove from to_process_urls table

    content = parse_urls.make_request(cleaned_url)
    if not content:
        return False
    try:
        title, cleaned_content = parse_urls.clean_request(content)
        tokenized = parse_urls.create_word_tokens(cleaned_content)
        tokenized_string = b" ".join(tokenized)

        insert_into_table(cursor, stored_urls_table, cleaned_url)
        insert_into_table(cursor, raw_text_table, cleaned_url, col_name=unprocessed_text, value=cleaned_content)
        insert_into_table(cursor, tokenized_text_table, cleaned_url, col_name=processed_text, value=tokenized_string)
        insert_into_table(cursor, titles_table, cleaned_url, col_name=title_column, value=title)
        delete_from_to_process_table(cursor, original_url)

    except Exception as e:
        print("ERROR ON URL: {}".format(cleaned_url))
        print(e)
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#        print(exc_type, fname, exc_tb.tb_lineno)
        cursor.close()
        raise e
        return False
    return True




def already_processed_url(cursor, url):
    cursor.execute('SELECT * FROM {tn} WHERE {pk}=(?)'.\
            format(tn=stored_urls_table, pk=primary_key), (url,) )
    return (cursor.fetchone() != None)


def start_processing():
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM {tn}'.\
                format(tn=to_process_urls_table))

        urls = map(lambda tup: tup[0], cursor.fetchall())
        for current_url in urls:
            cleaned_url = clean_url(current_url)

            if is_blacklisted(cleaned_url, cursor) or already_processed_url(cursor, cleaned_url):
                print("HERE:", current_url)
                delete_from_to_process_table(cursor, current_url)
                conn.commit()
            else:
                processed_correctly = process_url(cleaned_url, current_url, cursor)
                if processed_correctly:
                    conn.commit()
                else:
                    conn.rollback()

    except Exception as e:
        cursor.close()
        print("UNCLEAED:", current_url)
        print("CLEANED:", cleaned_url)
        raise e

if __name__ == "__main__":
    start_processing()
