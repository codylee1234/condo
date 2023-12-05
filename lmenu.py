
from flask import Blueprint, render_template, redirect, url_for, session, logging, request
from models import db, users,announcement,request_srv
from datetime import datetime,date 

lmenu_bp = Blueprint("lmenu", __name__)

@lmenu_bp.route('/enquiries')
def enquiries():
        try:    
             if request.method == "GET":
               if session['userid'] and  session['role']: 
                    headers = ['DateRequested', 'Subject', 'Details','RequestType']
                    useid = int(session['uid'])
                    if session['role'] == "ADMIN" :
                         detailsDT = request_srv.query.filter(request_srv.req_type.in_([1,2])).all()
                    else:
                         detailsDT = request_srv.query.filter(request_srv.req_type.in_([1,2]) & 
                                                              (request_srv.userid == useid)).all()

                    return render_template('enquiries.html',headers=headers,result=detailsDT)
               else:
                    return render_template('login.html')
        except Exception as e:
              print("eror:" ,e)

@lmenu_bp.route('/home')
def home():
    if request.method == "GET":
     if session['userid'] and  session['role']: 
          detailsDT = announcement.query.all()
          return render_template('home.html',result=detailsDT)
     else:
          return render_template('login.html')
     

@lmenu_bp.route('/profile',methods=['GET', 'POST'])
def profile():
    if request.method == "GET":
     if session['userid'] and  session['role']: 
          headers = ['S.No', 'Subject', 'Details','RequestType']
          detailsDT = request_srv.query.all()
          return render_template('profile.html',headers=headers,result=detailsDT)
     else:
          return render_template('login.html')
    elif request.method == "POST":
         return render_template('home.html') 
    else:
         return render_template('home.html') 
