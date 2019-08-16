from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from contextlib import closing

app = Flask(__name__)
mysql = MySQL()


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'shivam01'
app.config['MYSQL_DATABASE_DB'] = 'hack'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#create table user(id int NOT NULL AUTO_INCREMENT,name varchar(45) NULL,username varchar(45) NULL,email varchar(45) NOT NULL,password varchar(50) NOT NULL,mobile varchar(15) NOT NULL, PRIMARY KEY(id));
#alter table user add options VARCHAR(2)
#alter table user add address VARCHAR(250)
#Stored Procedure used to create User
#DELIMITER $$
# mysql> CREATE DEFINER=`root`@`localhost` PROCEDURE `createUser`(
#     -> IN p_name VARCHAR(100),
#     -> IN p_username VARCHAR(100),
#     -> IN p_email VARCHAR(100),
#     -> IN p_password VARCHAR(1000),
#     -> IN p_mobile VARCHAR(100)
#     -> IN p_option VARCHAR(2)
#     -> IN p_address VARCHAR(1000)
#     -> )
#     -> BEGIN
#     -> IF(select exists(select 1 from user where email=p_email)) THEN
#     -> select 'Email exists!!';
#     -> ELSE
#     -> insert into user
#     -> (
#     -> name, username, email, password, mobile,option,address)
#     -> values
#     -> (
#     -> p_name,
#     -> p_username,
#     -> p_email,
#     -> p_password,
#     -> p_mobile,
#     -> p_option,
#     -> p_address
#     -> );
#     -> END IF;
#     -> END$$

@app.route('/')
@app.route('/home/')
def home():
	return render_template('home.html');

@app.route('/about/')
def about():
	return render_template('about.html');

@app.route('/service/')
def service():
	return render_template('service.html');

@app.route('/contact/')
def contact():
	return render_template('contact.html');

@app.route('/',methods=['POST'])
def signUp():
    try:
        _name = request.form['name']
        _username=request.form['username']
        _email = request.form['email']
        _password = request.form['password']
        _mobile=request.form['mobileNumber']
        _address=request.form['address']
        _option=request.form['DorC']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call the MySQL

            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    _hashed_password = generate_password_hash(_password)
                    cursor.callproc('createUser',(_name,_username,_email,_hashed_password,_mobile,_address,_option))
                    data = cursor.fetchall()

                    if len(data) is 0:
                        conn.commit()
                        return json.dumps({'message':'User created successfully !'})
                    else:
                        return json.dumps({'error1':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error2':str(e)})

if __name__ == '__main__':
    app.run()
	 
	   