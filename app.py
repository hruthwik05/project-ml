from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import  mysql.connector
import pickle
import numpy as np  
  
app = Flask(__name__)
app.secret_key = 'your_secret_key'

  
  
conn=mysql.connector.connect(host='localhost',user='root',password='',database='user-system')
cursor=conn.cursor()
 




  
@app.route('/')


@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate user credentials
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            session['email']=email
            return render_template('user.html')
        else:
            return "Invalid email or password. Please try again."

    return render_template('login.html')

@app.route('/dishistory')
def history():
    if 'username' in session:
               cursor = conn.cursor()
               cursor.execute("SELECT * FROM records WHERE username = %s", (session['username'],))
               history = cursor.fetchall()
               return render_template('history.html', history=history)
    else:
        return render_template('help.html')


@app.route('/services')
def services():
    return render_template('service.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dishelp')
def help():
    return render_template('help.html')

@app.route('/disblood')
def blood():
    return render_template('bloodtest.html')

@app.route('/diskidney')
def kidney():
    return render_template('kidney.html')

@app.route('/disliver')
def liver():
    return render_template('liver.html')

@app.route('/dislung')
def lung():
    return render_template('lung.html')



      


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor.execute("SELECT * FROM user WHERE email = '%s'", (email))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        
        elif not name or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', ( name, email, password ))
            conn.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)
    
model=pickle.load(open('model.pkl','rb'))

@app.route('/predict',methods=['POST','GET'])
def predict():
    int_features=[int(x) for x in request.form.values()]
    
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict(final)
    print(prediction)
    probability=model.predict_proba(final)

    probal='{0:{1}f}'.format(probability[0][1],2)

    output=prediction[0]
    
    
    if output == 0:
        return render_template('bloodtest.html',pred='Your Report is Abnormal.\nProbability of normality is {}'.format(probal))
    else:
        return render_template('bloodtest.html',pred='Your Report is Normal.\nProbability of abnormality is {}'.format(probal))
    
model1=pickle.load(open('model1.pkl','rb'))

@app.route('/predict1',methods=['POST','GET'])
def predictk():
       
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict(final)
    print(prediction)
    probability=model.predict_proba(final)

    probal='{0:{1}f}'.format(probability[0][1],2)

    output=prediction[0]
    
    
    if output == 0:
        return render_template('kidney.html',pred='Your Report is Abnormal.\nProbability of normality is {}'.format(probal))
    else:
        return render_template('kidney.html',pred='Your Report is Normal.\nProbability of abnormality is {}'.format(probal))
       

model2=pickle.load(open('model2.pkl','rb'))

@app.route('/predict2',methods=['POST','GET'])

def predictl():
   
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict(final)
    print(prediction)
    probability=model.predict_proba(final)

    probal='{0:{1}f}'.format(probability[0][1],2)

    output=prediction[0]
    
    
    if output == 0:
        return render_template('liver.html',pred='Your Report is Abnormal.\nProbability of normality is {}'.format(probal))
    else:
        return render_template('liver.html',pred='Your Report is Normal.\nProbability of abnormality is {}'.format(probal))
    
model3=pickle.load(open('model3.pkl','rb'))

@app.route('/predict3',methods=['POST','GET'])
def predictg():
    
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict(final)
    print(prediction)
    probability=model.predict_proba(final)

    probal='{0:{1}f}'.format(probability[0][1],2)

    output=prediction[0]
    
    
    if output == 0:
        return render_template('lung.html',pred='Your Report is Abnormal.\nProbability of normality is {}'.format(probal))
    else:
        return render_template('lung.html',pred='Your Report is Normal.\nProbability of abnormality is {}'.format(probal))


if __name__ == "__main__":
    app.run(debug=True)