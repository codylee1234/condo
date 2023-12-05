
from flask import Blueprint, render_template, redirect, url_for, session, logging, request
from models import db, users,announcement,request_srv
from datetime import datetime,date 

adminmgmt_bp = Blueprint("adminmgmt", __name__)

@adminmgmt_bp.route('/manageusers',methods=['GET', 'POST'])
def manageusers():
    if request.method == "POST":
         try:              
          enqtype = request.form.get('enqtype',type=int)
          desc = request.form.get('des')
          subjectd = request.form.get('subj')
          uid = int(session['uid'])
          return redirect(url_for('lmenu.home'))
         except Exception as e:
              logging.error("error occured", exc_info=e)
    elif request.method == "GET":
         if session['userid'] and  session['role']: 
                    headers = ['DateRequested', 'Subject', 'Details','RequestType']
                    detailsDT = request_srv.query.all()
                    return render_template('manageusers.html',headers=headers,result=detailsDT)