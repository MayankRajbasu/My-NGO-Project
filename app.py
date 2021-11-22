from flask import Flask, render_template,url_for,request,redirect
from flask_mysqldb import MySQL

import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MOINAK;'
                      'Database=NGO;'
                      'Trusted_Connection=yes;'
                      )
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def hello_world():
    # put application's code here
    return render_template('index.html')

@app.route("/donate", methods=['GET','POST'])
def donate():
    if request.method == 'POST':
        userDetails =request.form
        Name = userDetails['name']
        Age= userDetails['age']
        Aadhar=userDetails['aadhar']
        Phone=userDetails['phone']
        City=userDetails['city']
        Address=userDetails['address']
        Item=userDetails['item']
        Quantity=userDetails['quantity']
        Amount =userDetails['amount']

        cur.execute(" INSERT INTO Donor(Name, Age,Aadhar, Phone, City, Address) VALUES(?,?,?,?,?,?)",(Name,Age,Aadhar,Phone,City,Address))
        cur.commit()
        cur.execute("INSERT INTO Donation(Aadhar,Item_donated,Item_quantity,Amount_donated) VALUES(?,?,?,?)",(Aadhar,Item,Quantity,Amount))
        cur.commit()
        # return 'sucess'
        # print(Name,Age)
        return redirect('/ngo')

    return render_template('Form.html')

@app.route("/volunteer", methods=['GET','POST'])
def volunteer():
    if request.method == 'POST':
        VolunteerDetails =request.form
        Name = VolunteerDetails['name']
        Age= VolunteerDetails['age']
        Gender=VolunteerDetails['gender']
        Aadhar = VolunteerDetails['aadhar']
        Phone=VolunteerDetails['phone']
        City=VolunteerDetails['city']
        Address=VolunteerDetails['address']
        cur.execute(" INSERT INTO Volunteer(Name, Age,Gender,Aadhar, Phone, City, Address) VALUES(?,?,?,?,?,?,?)",(Name,Age,Gender,Aadhar,Phone,City,Address))
        cur.commit()
        return redirect('/ngo')
    return render_template('V_form.html')

@app.route("/ngo",methods=['GET','POST'])
def ngo():
    if request.method == 'POST':
        n_data=request.form
        City = n_data['city']
        cur.execute("SELECT * fROM Ngo where City=(?) ",(City))
        data =cur.fetchall()
        return render_template("List.html",ngo=data)
    cur.execute("SELECT * fROM Ngo")
    data = cur.fetchall()
    return render_template("List.html",ngo=data)

@app.route("/regNgo",methods=['GET','POST'])
def regngo():
    return render_template('N_form.html')

if __name__ == '__main__':
    app.run(debug=True)
