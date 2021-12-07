from flask import Flask, render_template,url_for,request
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MOINAK;'
                      'Database=NGO;'
                      'Trusted_Connection=yes;'
                      )
cur = conn.cursor()

app = Flask(__name__)


@app.route('/')
def home():
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
        cur.execute("SELECT * fROM Ngo where City=(?) ", (City))
        data = cur.fetchall()
        return render_template("List.html", ngo=data)
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
        cur.execute("SELECT * fROM Ngo where City=(?) ", (City))
        data = cur.fetchall()
        return render_template("List.html", ngo=data)
    return render_template('V_form.html')

@app.route("/old_donor",methods=['GET','POST'])
def old_donor():
    if request.method == 'POST':
        n_data=request.form
        Aadhar=n_data['aadhar']
        Item = n_data['item']
        Quantity = n_data['quantity']
        Amount = n_data['amount']
        cur.execute("INSERT INTO Donation(Aadhar,Item_donated,Item_quantity,Amount_donated) VALUES(?,?,?,?)",(Aadhar,Item,Quantity,Amount))
        cur.commit()
    return render_template("O_form.html")

@app.route("/regNgo",methods=['GET','POST'])
def regngo():
    if request.method =='POST':
        r_data=request.form
        Name=r_data['name']
        Work=r_data['work']
        Phone=r_data['phone']
        City=r_data['city']
        State=r_data['state']
        cur.execute(" INSERT INTO NGO(Ngo_Name,Ngo_Workfield,Phone,City,State) VALUES (?,?,?,?,?)",(Name,Work,Phone,City,State))
        cur.commit()
    return render_template('N_form.html')

if __name__ == '__main__':
    app.run(debug=True)
