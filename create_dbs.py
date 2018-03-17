import sqlite3

sqlite_file = 'history.sqlite'    # name of the sqlite database file
to_process_urls_table = 'to_process_urls'  # name of the table to be created
stored_urls_table = 'processed_urls'  # name of the table to be created
blacklisted_table = 'blacklisted_urls'
raw_text_table = 'raw_text'
tokenized_text_table = 'tokenized_text'

primary_key = 'url' # name of the column
processed_text = 'processed_text'
unprocessed_text = 'unprocessed_text'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Unprocessed URLs table
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=to_process_urls_table, nf=primary_key, ft="TEXT"))

# Processed URLs table
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=stored_urls_table, nf=primary_key, ft="TEXT"))

# Blacklisted URLs table
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
         .format(tn=blacklisted_table, nf=primary_key, ft="TEXT"))

# Raw Text Table
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY, {nf2} {ft})'\
        .format(tn=raw_text_table, nf=primary_key, ft="TEXT", nf2=processed_text))

# Tokenize Text Table
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY, {nf2} {ft})'\
        .format(tn=tokenized_text_table, nf=primary_key, ft="TEXT", nf2=unprocessed_text))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
