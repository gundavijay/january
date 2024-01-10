from flask import Flask, render_template,jsonify,request
import pickle
import sqlite3
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/prediction",methods = ['GET','POST'])
def prediction():
    if request.method=='POST':
        nitro = request.form.get('nitrogen')
        phos  = request.form.get('phosphorus')
        kp    = request.form.get('potassium')
        temp  = request.form.get('temperature')
        hum = request.form.get('humidity')
        ph = request.form.get('ph')
        rain = request.form.get('rainfall')
        print(nitro,phos,kp,temp,hum,ph,rain)
        with open('model.pkl','rb') as model_file:
            mlmodel = pickle.load(model_file)
        res = mlmodel.predict([[float(nitro),float(phos),float(kp),float(temp),float(hum),float(ph),float(rain)]])
        print(res)
        conn = sqlite3.connect('cropdata.db')
        cur = conn.cursor()
        cur.execute(f'''insert into crop values({nitro},{phos},{kp},{temp},{hum},{ph},{rain},'{res[0]}')''')
        conn.commit()
        return render_template("result.html",res=res[0])    
    else:
        return render_template('prediction.html')
                    
    @app.route("/showdata",methods = ['GET','POST'])
    def showdata():
         conn = sqlite3.connect('cropdata.db')
         cur = conn.cursor()
         cur.execute("select*from crop")
         X=cur.fetchall()
         li =[]
         for i in X:
              p={}
              p['Nitrogen']=i[0]
              p['phosphor']=i[1]
              p['potassium']=i[2]
              p['Temperature']=i[3]
              p['Humidity']=i[4]
              p['ph']=i[5]
              p['Rainfull']=i[6]
              p['Result']=i[7]
              li.append(P)
    return render_template('showdata.html',data=li)    
    

    


if __name__=='__main__':
    app.run(host='0.0.0.0',port=4567)