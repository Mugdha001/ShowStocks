from flask import Flask
from flask import render_template
from flask import request
import requests
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':

        #Input Fields
        symbol = request.form['symbol'].upper()
        print(symbol)
        
        # Make API CALL with the symbol
        datum = requests.get('https://fmpcloud.io/api/v3/quote/'+symbol+'?apikey=APIKEY')
        #print("------------",type(datum),"------1----------")
        data = json.loads(datum.text)
        print(data)
        if len(data) < 1:
            tempData = {'msg' : "No stock Symbol found. Please enter correct details."}
            return render_template('index.html', **tempData)
        else:
            dateTime = datetime.now()
            fullName = data[0]["name"]
            price = data[0]["price"]
            change = data[0]["change"]
            changePer = data[0]["changesPercentage"]
            tempData = {'dateTime': dateTime, 'fullName': fullName, 'price': price, 'change' : change, 'changePer': changePer }
            return render_template('output.html', **tempData)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000)
