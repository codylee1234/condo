from flask import Flask, render_template, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime,date 
import logging
from models import db,users,announcement,cars,request_srv
from adminmgmt import adminmgmt_bp
from lmenu import lmenu_bp



app = Flask(__name__)
app.secret_key = 'ABCD1234ABCD'
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Destiny10!@localhost:5432/postgres"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://manipazhani:oqg1pUcn2RTA@ep-ancient-poetry-05143267.ap-southeast-1.aws.neon.tech/condo?sslmode=require"
#db = SQLAlchemy(app)
db.init_app(app)

app.register_blueprint(adminmgmt_bp)
app.register_blueprint(lmenu_bp)

#For Logging
logging.basicConfig(format="%(asctime)s::%(levelname)s::%(message)s",
                    level=logging.INFO,
                    filename='app.log',
                    )

#login into system
@app.route('/',methods=['GET', 'POST'])
@app.route('/login/',methods=['GET', 'POST'])
def login():    
          if request.method == "POST":
               uname = request.form["uname"]
               passw = request.form["passw"]
               loginUser = users.query.filter_by(userid=uname, password=passw).first()

               if loginUser is not None:
                    session['loggedin'] = True
                    session['userid'] = loginUser.userid
                    session['name'] = loginUser.fname
                    session['role'] = loginUser.role
                    session['uid'] = loginUser.id
                    logging.info('User logged:' + session['userid']+ ' at ' + str(datetime.now()))
                    
                    return redirect(url_for("lmenu.home"))
               else:
                    return redirect(url_for("login"))
        
               return render_template("login.html")
          else:
               return render_template("login.html")
     
     
#admin enquiry 
@app.route('/adminenq', methods=['GET', 'POST'])
def adminenq():
    if request.method == "POST":
         try:              
          feedbackText = request.form.get('fbTxt')
          uniqueidy = request.form.get('enqyid')
          uid = int(session['uid'])
          
          updEnqry =request_srv.query.get(int(uniqueidy))

          if updEnqry:
               updEnqry.feedback= feedbackText
               updEnqry.status = 'CLOSED'
               db.session.commit()
               #logging.info('Update to db logged:' + session['userid']+ ' at ' + str(datetime.now()))
                    
          return redirect(url_for('lmenu.home'))
         except Exception as e:
              logging.error("Error occured", exc_info=e)
    elif request.method == "GET":
         if session['userid'] and  session['role']: 
               headers = ['DateRequested', 'Subject', 'Details','RequestType']
               detailsDT = request_srv.query.all()
               return render_template('adminenq.html',headers=headers,result=detailsDT)
         

#submit enquiry by resident    
@app.route('/check',methods=['GET', 'POST'])
def check():
    if request.method == "POST":
         try:              
          enqtype = request.form.get('enqtype',type=int)       

          desc = request.form.get('des')
          subjectd = request.form.get('subj')
          uid = int(session['uid'])

          new_enq = request_srv( req_dt=date.today(),
                         req_type=enqtype,  # Replace with your desired req_type value
                         userid=uid,  # Replace with the actual user ID
                         subject=subjectd,
                         details=desc,
                         work_type=1,
                         from_dt=datetime.utcnow(),
                         to_dt=datetime.utcnow(),
                         v_name='',
                         vehicle_no='',
                         ph_number=0000,
                         id_details = '',
                         status = 'OPEN',
                         rating = 0,
                         feedback='')
          
          db.session.add(new_enq)
          #db.session.add(new_post)

          db.session.commit()
          return redirect(url_for('lmenu.home'))
         except Exception as e:
              logging.error("Some error occured", exc_info=e)
    elif request.method == "GET":
         if session['userid'] and  session['role']: 
                    headers = ['DateRequested', 'Subject', 'Details','RequestType']
                    detailsDT = request_srv.query.all()
                    return render_template('dd.html',headers=headers,result=detailsDT)         

#generate feedback view by enquiryid
@app.route('/feedbackview',methods=['GET', 'POST'])
def feedbackview():
    if request.method == "GET":
     if session['userid'] and  session['role']: 
          desc =request.args.get('des')
          fbDlts = request_srv.query.filter_by(id=int(desc)).all()
          return render_template('feedback.html',result=fbDlts)
     else:
          return render_template('login.html')
    elif request.method == "POST":
         return render_template('home.html') 
    else:
         return render_template('home.html')

#logout    
@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('role',None)
    session.pop('name',None)
    session.pop('loggedin',False)    
    return redirect(url_for("login"))  

#announcement data handling
@app.route('/managedata',methods=['GET', 'POST'])
def managedata():
        try:    
             if request.method == "GET":
               if session['userid'] and  session['role']: 
                    headers = ['DateRequested', 'Subject', 'Details','RequestType']
                    detailsDT = request_srv.query.filter(request_srv.req_type.in_([1,2])).all()
                    return render_template('managedata.html',headers=headers,result=detailsDT)
             elif request.method == "POST":
                 try:              
                    if 'picture' in request.files:
                         #do picture save
                         return render_template('managedata.html')
                    else:
                         return render_template('aa.html')
                 except Exception as e:
                    print(f"Error:{e}")
                    return render_template('managedata.html')
             else:
                    return render_template('login.html')
        except Exception as e:
              print("eror:" ,e)

#save new announcements
@app.route('/saveanc',methods=['GET', 'POST'])
def saveanc():
        try:    
             if request.method == "GET":
               if session['userid'] and  session['role']: 
                    headers = ['DateRequested', 'Subject', 'Details','RequestType']
                    detailsDT = request_srv.query.filter(request_srv.req_type.in_([1,2])).all()
                    return render_template('managedata.html',headers=headers,result=detailsDT)
             elif request.method == "POST":
                 try:              
                         desc = request.form.get('anc')
                         uid = int(session['uid'])

                         new_anc = announcement(activity_dt = date.today(),
                                                details=desc,
                                                userid=uid
                                                )
                         db.session.add(new_anc)
                         db.session.commit()
                         return redirect(url_for('lmenu.home'))
                 except Exception as e:
                    print(f"Error:{e}")
                    return render_template('managedata.html')
             else:
                    return render_template('login.html')
        except Exception as e:
              print("eror:" ,e)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,port=5001)
#--------------------------------------------------

