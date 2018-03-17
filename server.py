from flask import Flask, request
import sqlite3
app = Flask(__name__)

response_headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 
        'Access-Control-Allow-Origin': '*', 
        'Access-Control-Allow-Methods': 'POST,GET'
        }

    
@app.route('/', methods=['POST', 'GET'])
def result():
    if request.method == 'GET':
        print("YOYOYO")
        return 'Received !'
    elif request.method == 'POST':
        data = request.get_data()
        print("DATA:", data)
        
        conn = sqlite3.connect('history.sqlite')
        with conn as cursor:
            cursor.execute("INSERT OR IGNORE INTO {tn} VALUES (?)".\
                format(tn='to_process_urls'), (data,))

#        with open("data.txt", "ab") as f:
#            f.write(data)
#            f.write(b"\n")
        return "blank", 200, response_headers
    else:
        print("ERROR: UNKOWN REQUEST METHOD")
        return "MERP"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
