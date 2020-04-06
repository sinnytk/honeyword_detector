import flask
from flask import request
import os
import os.path
import hashlib
import playsound

app = flask.Flask(__name__)
app.config["DEBUG"] = True

honey_words = ['password', '123456', '12345678', '12345', 'qwerty', 'abc123', 'football', 'monkey', '123456789', 'letmein', '111111', '1234', '1234567890', 'dragon', 'baseball', 'trustno1', 'iloveyou', 'princess', 'adobe123', '123123', '1234567', 'welcome', 'login', 'admin', 'solo', 'master', 'sunshine',
               'photoshop', '1qaz2wsx', 'ashley', 'mustang', '121212', 'starwars', 'bailey', 'access', 'flower', 'passw0rd', 'shadow', 'michael', '654321', 'jesus', 'password1', 'superman', 'hello', '696969', 'qwertyuiop', 'hottie', 'freedom', 'qazwsx', 'ninja', 'azerty', 'loveme', 'whatever', 'zaq1zaq1', 'Football', '000000']


def register(username_rec, password_rec, first_rec, last_rec):
    is_honeyword = False
    for word in honey_words:
        if word == password_rec:
            is_honeyword = True
            break

    if is_honeyword == False:
        salt = str(os.urandom(32))
        salt2 = str.encode(salt)
        entered_password = password_rec
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256', entered_password.encode('ascii'), salt2, 100000)
        print(str(hashed_password))
        with open(username_rec+".txt", "w") as file:
            file.write(str(hashed_password)+" " +
                       first_rec+" "+last_rec+" "+salt)
        return 'OK'
    else:
        return 'Error'


def login(username_log, password_log):
    file_name = username_log+".txt"
    cur_dir = os.getcwd()
    flag = True
    for word in honey_words:
        if word == password_log:
            flag = False
            return 'Honeyword detected'

    while flag == True:
        file_list = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in file_list:
            print("User exixts")
            f = open(file_name, "r")
            data = f.read()
            x = data.split(" ")
            entered_password_log = password_log
            preserved_salt = x[3]
            preserved_salt_encoded = str.encode(preserved_salt)
            hashed_password_entered = hashlib.pbkdf2_hmac(
                'sha256', entered_password_log.encode('ascii'), preserved_salt_encoded, 100000)
            if(x[0] == str(hashed_password_entered)):
                print("logged in successfully")
                user = username_log
                first = x[1]
                last = x[2]
                message = "Welcome "+username_log
                login = True
                return 'OK'
            else:
                print("wrong password")
                return 'Wrong password'
            break
        else:
            if cur_dir == parent_dir:
                print("User doesnt exist. Please register to proceed")
                return 'No such user'
            else:
                cur_dir = parent_dir


@app.route('/register', methods=['POST'])
def json_get():
    req_data = request.get_json()
    response = register(req_data['username'], req_data['password'],
                        req_data['first_name'], req_data['last_name'])
    return response


@app.route('/login', methods=['POST'])
def json_get_login():
    req_data = request.get_json()
    response = login(req_data['username'], req_data['password'])
    return response


app.run()
