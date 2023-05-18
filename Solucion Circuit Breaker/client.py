from flask import Flask
from flask import request, jsonify
import urllib.request, json
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Do not remove this method.
count=0
flag=True
@app.errorhandler(Exception)
def handle_error(e):
    global count
    global flag
    count= count +1
    flag = False
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=e), code

@app.route('/igv')
def igv():
    tax = get_tax_from_api()

    return jsonify(igv=tax), 200

def get_tax_from_api():
    global flag 
    global count
    url = "http://127.0.0.1:5000/tax"
    if (count<2 and flag) or ((count<5 and flag) or count%5==0):
        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)
        return int(dict["Tax"])
    else:
        flag = True
        if(count>5):
            count = count+1
        return "CircuitException"

if __name__ == "__main__":
    app.run(debug=True, port=3000)