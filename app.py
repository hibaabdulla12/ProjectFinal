import datetime
from cmath import sqrt

from flask import Flask, render_template, request, session, jsonify
from sklearn.ensemble import RandomForestClassifier

from DBConnection import Db

app = Flask(__name__)
app.secret_key="hi"
static_path="D:\\project\\WEB\\fitme\\static\\"


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/ahm')
def ahm():
    return render_template("admin/home.html")






@app.route('/login_post', methods=['post'])
def login_post():
    db=Db()
    username=request.form['textfield']
    password=request.form['textfield2']
    qry="SELECT * FROM login WHERE username='"+username+"' AND PASSWORD='"+password+"'"
    res=db.selectOne(qry)
    if res is None:
        return "<script>alert('Incorrect Details');window.location='/';</script>"
    else:
        type=res['type']
        if type=="admin":
            return  render_template("admin/home.html")
        elif type == "tailor":
            session['tailorid'] = res['login_id']
            return render_template("tailor/home.html")
        else:
            return "<script>alert('unauthorised user');window.location='/';</script>"

@app.route('/adm_home')
def adm_home():
    return render_template("admin/home.html")

@app.route('/tailor_home')
def tailor_home():
    return render_template("tailor/home.html")


@app.route("/adm_add_dress")
def adm_add_dress():
    return render_template("admin/add_dress.html")

@app.route("/adm_add_dress_post", methods=['post'])
def adm_add_dress_post():
    dname=request.form['textfield']
    qry="INSERT INTO dress(`name`) VALUES('"+dname+"')"
    print(qry)
    db=Db()
    db.insert(qry)
    return "ok"
@app.route("/adm_add_tailor")
def adm_add_tailor():
    return render_template("admin/add_tailor.html")

@app.route("/adm_add_tailor_post", methods=['post'])
def adm_add_tailor_post():
    name=request.form['textfield']
    dateofbirth=request.form['textfield2']
    gender=request.form['radio']
    email=request.form['textfield3']
    phone=request.form['textfield4']
    house=request.form['textfield5']
    post=request.form['textfield6']
    pin=request.form['textfield7']
    image=request.files['fileField']
    image.save(static_path+"tailor_image\\"+image.filename)
    path="/static/tailor_image/"+image.filename
    qry="INSERT INTO login(`username`,`password`,`type`) VALUES('"+email+"','"+phone+"','tailor')"
    db=Db()
    lid=db.insert(qry)
    qry1="INSERT INTO tailor(NAME,dob,gender,email,phone,house,post,pin,image,login_id)VALUES('"+name+"','"+dateofbirth+"','"+gender+"','"+email+"','"+phone+"','"+house+"','"+post+"','"+pin+"','"+ path+"','"+str(lid)+"')"
    db.insert(qry1)
    return "<script>alert('Tailor added successfully');window.location='/adm_view_tailor#cont'</script>"
@app.route("/adm_assign_work_to_tailors/<booking_id>")
def adm_assign_work_to_tailors(booking_id):
    session['bookingid']=booking_id
    db=Db()
    qry="SELECT * FROM tailor "
    res=db.select(qry)
    return render_template("admin/assign_work_to_tailors.html",data=res)

@app.route("/adm_assign_work_to_tailors_post",methods=['post'])
def adm_assign_work_to_tailors_post():
    booking_id=session['bookingid']
    tailorid=request.form['select']
    enddate=request.form['textfield']
    db=Db()
    qry="INSERT INTO booking_assign(booking_id,tailor_id,assign_date,end_date,`status`) VALUES ('"+booking_id+"','"+tailorid+"',curdate(),'"+enddate+"','pending')"
    db.insert(qry)
    db.update("update booking set status='assigned' WHERE booking_id='"+booking_id+"'")
    return "<script>alert('Booking Assigned');window.location='/adm_view_booking';</script>"




@app.route("/adm_change_pasword")
def adm_change_pasword():
    return render_template("admin/change_password.html")

@app.route("/adm_change_pasword_post",methods=['post'])
def adm_change_pasword_post():
    currentpassword=request.form['textfield']
    newpassword=request.form['textfield2']
    db=Db()
    qry="SELECT* FROM login WHERE TYPE='admin' AND PASSWORD='"+currentpassword+"'"
    res=db.selectOne(qry)
    if res is None:
        return "<script>alert('Incorrect Password');window.location='/adm_change_pasword';</script>"
    else:
        qry2="UPDATE login SET PASSWORD='"+newpassword+"' WHERE login_id='"+str(res['login_id'])+"'"
        db.update(qry2)
        return "<script>alert('Password changed');window.location='/'</script>"


    return render_template("admin/change_password.html" )



@app.route("/adm_edit_dress/<dress_id>")
def adm_edit_dress(dress_id):
    session['dressid']=dress_id
    db=Db()
    qry="SELECT * FROM dress WHERE dress_id='"+dress_id+"'"
    res=db.selectOne(qry)
    return render_template("admin/edit_dress.html", data=res)

@app.route("/adm_edit_dress_post",methods=['post'])
def adm_edit_dress_post():
    dress_id=session['dressid']
    db=Db()
    name=request.form["textfield"]
    qry="UPDATE dress SET NAME='"+name+"' WHERE dress_id='"+dress_id+"'"
    db.update(qry)
    return adm_view_dress()


@app.route("/adm_edit_tailor/<tailor_id>")
def adm_edit_tailor(tailor_id):
    session['tailorid']=tailor_id
    db=Db()
    qry="SELECT * FROM tailor WHERE tailor_id='"+tailor_id+"'"
    res=db.selectOne(qry)
    return render_template("admin/edit_tailor.html",data=res)

@app.route("/chat/<id>")
def chat(id):
    session["userid"]=id
    return render_template("admin/fur_chat.html", toid=id)


@app.route("/chat_usr_chk",methods=['post'])        # refresh messages chatlist
def chat_usr_chk():
    uid=request.form['idd']
    qry = "select from_id,message as msg,date from chat where (from_id='0' and to_id='" + uid + "') or ((from_id='" + uid + "' and to_id='0')) order by chat_id desc"
    c = Db()
    res = c.select(qry)
    return jsonify(res)



@app.route("/viewmsg/<senid>")        # refresh messages chatlist
def viewmsg(senid):
    uid=senid
    qry = "select from_id,message as msg,date from chat where (from_id='0' and to_id='" + uid + "') or ((from_id='" + uid + "' and to_id='0')) order by chat_id desc"
    c = Db()
    res = c.select(qry)
    return jsonify(data=res)


@app.route("/arc_chat_usr_post",methods=['POST'])
def arc_chat_usr_post():
    id=str(session["userid"])
    ta=request.form["ta"]
    qry="insert into chat(message,date,from_id,to_id) values('"+ta+"',CURDATE(),'0','"+id+"')"
    d=Db()
    d.insert(qry)
    session["userid"] = id
    return render_template("admin/chat.html", toid=id)
    # qry = "select date,message,sid from chat where (sid='" + str(
    #     session['ext_lid']) + "' and rid='" + str(id) + "') or ((sid='" + str(id) + "' and rid='" + str(
    #     session['ext_lid']) + "')) order by chatid desc"
    # res = d.select(qry)
    # return render_template('EXTERIOR/ext_chat_usr.html', res=res, id=int(session['fur_lid']))

@app.route("/chatview",methods=['post'])
def chatview():
    db=Db()
    qry="select * from users"
    res=db.select(qry)
    return jsonify(data=res)

@app.route("/insert_chat/<senid>/<msg>")
def insert_chat(senid,msg):
    db=Db()
    qry="insert into chat (date,time,from_id,to_id,message) values (curdate(),curtime(),'0','"+senid+"','"+msg+"')"
    db.insert(qry)
    return jsonify(status="ok")



@app.route("/adm_edit_tailor_post",methods=['post'])
def adm_edit_tailor_post():
    tailor_id = session['tailorid']
    db=Db()
    name=request.form['textfield']
    dob=request.form['textfield2']
    gender=request.form['radio']
    phone=request.form['textfield4']
    house=request.form['textfield5']
    post=request.form['textfield6']
    pin=request.form['textfield7']
    if 'fileField' in request.files:
        image=request.files['fileField']
        if image.filename=="":
            qry = "UPDATE tailor SET NAME='" + name + "',dob='" + dob + "',gender='" + gender + "',phone='" + phone + "',house='" + house + "',post='" + post + "',pin='" + pin + "' WHERE tailor_id='" + tailor_id + "'"
        else:
            image.save(static_path+"tailor_image\\"+image.filename)
            path="/static/tailor_image/"+image.filename
            qry="UPDATE tailor SET NAME='"+name+"',dob='"+dob+"',gender='"+gender+"',phone='"+phone+"',house='"+house+"',post='"+post+"',pin='"+pin+"',image='"+path+"' WHERE tailor_id='"+tailor_id+"'"
    else:
        qry="UPDATE tailor SET NAME='"+name+"',dob='"+dob+"',gender='"+gender+"',phone='"+phone+"',house='"+house+"',post='"+post+"',pin='"+pin+"' WHERE tailor_id='"+tailor_id+"'"
    db.update(qry)
    return adm_view_tailor()

@app.route("/adm_send_reply/<complaint_id>")
def adm_send_reply(complaint_id):
    session['complaintid']=complaint_id
    db=Db()
    qry="SELECT * FROM complaint WHERE complaint_id='"+complaint_id+"'"
    res=db.selectOne(qry)
    return render_template("admin/send_reply.html",data=res)

@app.route("/adm_send_reply_post", methods=['post'])
def adm_send_reply_post():
    complaint_id=session['complaintid']
    db=Db()
    reply=request.form['textarea']
    qry="UPDATE complaint SET reply='"+reply+"',STATUS='replied' WHERE complaint_id='"+complaint_id+"'"
    db.update(qry)
    return adm_view_complaints()


@app.route("/adm_view_booking")
def adm_view_booking():
    db=Db()
    qry="SELECT booking.*,dress.name AS dress_name,users.name FROM dress,users, booking WHERE dress.dress_id=booking.dress_id AND booking.user_id=users.login_id and status='pending'"
    res=db.select(qry)
    return render_template("admin/view_booking.html", data=res)

@app.route("/adm_view_booking_post",methods=['post'])
def adm_view_booking_post():
    booking=request.form["textfield"]
    booking2=request.form["textfield2"]
    db=Db()
    qry="SELECT booking.*,dress.name AS dress_name,users.name FROM dress,users, booking WHERE dress.dress_id=booking.dress_id AND booking.user_id=users.login_id and status='pending' AND date between '"+booking+"' and '"+booking2+"'"
    res=db.select(qry)
    return render_template("admin/view_booking.html", data=res)

@app.route("/adm_view_complaints")
def adm_view_complaints():
    db=Db()
    qry="SELECT `complaint`.*, users.name FROM users, complaint WHERE users.login_id=complaint.user_id"
    res=db.select(qry)
    return render_template("admin/view_complaints.html",data=res)


@app.route("/adm_view_complaints_post", methods=["post"])
def adm_view_complaints_post():
    fromdate=request.form["textfield"]
    todate=request.form["textfield2"]
    db=Db()
    qry="SELECT `complaint`.*, users.name FROM users, complaint WHERE users.login_id=complaint.user_id and date between '"+fromdate+"' and '"+todate+"'"
    res=db.select(qry)
    return render_template("admin/view_complaints.html",data=res)

@app.route("/adm_view_dress")
def adm_view_dress():
    db=Db()
    qry="SELECT * FROM `dress`"
    res=db.select(qry)
    return render_template("admin/view_dress.html", data=res)

@app.route("/adm_view_dress_post", methods=['post'])
def adm_view_dress_post():
    dressname=request.form['textfield']
    db=Db()
    qry="SELECT * FROM `dress`  WHERE NAME LIKE '%"+dressname+"%'"
    res=db.select(qry)
    return render_template("admin/view_dress.html", data=res)


@app.route("/adm_del_dress/<dress_id>")
def adm_del_dress(dress_id):
    db=Db()
    qry="DELETE FROM dress WHERE `dress_id`='"+dress_id+"'"
    db.delete(qry)
    return adm_view_dress()


@app.route("/adm_view_tailor")
def adm_view_tailor():
    db=Db()
    qry="SELECT * FROM `tailor`"
    res=db.select(qry)
    return render_template("admin/view_tailor.html",data=res)

@app.route("/adm_view_tailor_post",methods=["post"])
def adm_view_tailor_post():
    name=request.form['textfield']
    db=Db()
    qry="SELECT * FROM `tailor` WHERE NAME LIKE '%"+name+"%'"
    res=db.select(qry)
    return render_template("admin/view_tailor.html",data=res)


@app.route("/adm_del_tailor/<tailor_id>")
def adm_del_tailor(tailor_id):
    db=Db()
    qry="DELETE FROM tailor WHERE `tailor_id`='"+tailor_id+"'"
    db.delete(qry)
    return adm_view_tailor()



@app.route("/adm_view_users")
def adm_view_users():
    db=Db()
    qry="SELECT * FROM users"
    res=db.select(qry)
    return render_template("admin/view_users.html", data=res)

@app.route("/adm_view_users_post",methods=['post'])
def adm_view_users_post():
    name=request.form['textfield']
    db=Db()
    qry="SELECT * FROM users where name like '%"+name+"%'"
    res=db.select(qry)
    return render_template("admin/view_users.html", data=res)

@app.route("/adm_view_work_status")
def adm_view_work_status():
    db=Db()
    qry="SELECT * FROM tailor"
    res=db.select(qry)
    return render_template("admin/view_work_status.html",data=res)

@app.route("/adm_view_work_status_post",methods=['post'])
def adm_view_work_status_post():
    db=Db()
    tailor_id=request.form['select']
    qry="SELECT * FROM tailor"
    res=db.select(qry)
    qry1="SELECT booking.*,dress.name AS dress_name,users.name,booking_assign.end_date,booking_assign.status,booking_assign.assign_date FROM dress,users, booking,booking_assign WHERE dress.dress_id=booking.dress_id AND booking.user_id=users.login_id AND booking.booking_id=booking_assign.booking_id AND booking_assign.tailor_id='"+tailor_id+"'"
    res1=db.select(qry1)
    return render_template("admin/view_work_status.html",data=res,data1=res1)


@app.route("/change_passwordd")
def change_passwordd():
    return render_template("tailor/change_passwordd.html")

@app.route("/change_passwordd_post",methods=['post'])
def change_passwordd_post():
    tailorid = session['tailorid']
    currentpassword=request.form['textfield']
    newpassword=request.form['textfield2']
    db=Db()
    qry="SELECT * FROM login WHERE PASSWORD='"+currentpassword+"' AND login_id='"+str(tailorid)+"'"
    res=db.selectOne(qry)
    print(res)
    if res==None:
        return '''<script>alert("!!!incorrect password!!!"); window.location='/change_passwordd'; </script>'''
    else:
        qry2="UPDATE login SET PASSWORD='"+newpassword+"' WHERE login_id='"+str(tailorid)+"'"
        res1=db.update(qry2)
        print(res1)
        return '''<script>alert("OK");window.location='/';</script>'''



@app.route("/view_assigned_orders")
def view_assigned_orders():
    tailorid=session['tailorid']
    db=Db()
    qry="SELECT booking.*,dress.name AS dress_name,users.name,users.login_id,booking_assign.end_date,booking_assign.assign_id,booking_assign.status,booking_assign.assign_date FROM dress,users, booking,booking_assign WHERE dress.dress_id=booking.dress_id AND booking.user_id=users.login_id AND booking.booking_id=booking_assign.booking_id AND booking_assign.tailor_id='"+str(tailorid)+"' and booking_assign.status='pending'"
    res=db.select(qry)
    return render_template("tailor/view_assigned_orders.html",data=res)



@app.route("/view_assigned_order_more/<assign_id>/<user_id>")
def view_assigned_order_more(assign_id,user_id):
   session['assignid']=assign_id
   db=Db()
   qry = "SELECT users.login_id,booking.*,dress.name AS dress_name,users.name,users.email,users.phone,booking_assign.end_date,booking_assign.status,booking_assign.assign_date FROM dress,users, booking,booking_assign WHERE dress.dress_id=booking.dress_id AND booking.user_id=users.login_id AND booking.booking_id=booking_assign.booking_id AND booking_assign.assign_id='" + str(assign_id) + "'"


   res1=db.selectOne(qry)

   qry2 = "SELECT * FROM measurement WHERE user_id ='" + str(res1['login_id'] )+ "'"
   print(qry2)
   res2=db.selectOne(qry2)
   return render_template("tailor/view_assigned_order_more.html",data1=res1,data2=res2)


@app.route("/view_assigned_order_more_post",methods=['post'])
def view_assigned_order_more_post():
   assign_id=session['assignid']
   db=Db()
   qry = "UPDATE booking_assign SET STATUS='completed' WHERE assign_id='"+assign_id+"'"
   db.update(qry)
   res=db.selectOne("select * from booking_assign WHERE assign_id='"+assign_id+"'")
   bookid=res['booking_id']
   db.update("update booking set status ='completed' WHERE booking_id='"+str(bookid)+"'")
   return view_assigned_orders()



@app.route("/view_previous_works")
def view_previous_works():
    tailorid = session['tailorid']
    db=Db()
    qry="SELECT booking.*,dress.name AS dress_name,users.name,users.login_id,booking_assign.end_date,booking_assign.assign_id,booking_assign.status,booking_assign.assign_date FROM dress,users, booking,booking_assign WHERE dress.dress_id=booking.dress_id AND booking.user_id=users.login_id AND booking.booking_id=booking_assign.booking_id AND booking_assign.tailor_id='"+str(tailorid)+"' and booking_assign.status='completed'"
    res=db.select(qry)
    return render_template("tailor/view_previous_works.html",data=res)

@app.route("/view_previous_works_post",methods=['post'])
def view_previous_works_post():
    tailorid = session['tailorid']
    fromdate=request.form["textfield"]
    todate = request.form["textfield2"]
    db=Db()
    qry="SELECT booking.*,dress.name AS dress_name,users.name,users.login_id,booking_assign.end_date,booking_assign.assign_id,booking_assign.status,booking_assign.assign_date FROM dress,users, booking,booking_assign WHERE dress.dress_id=booking.dress_id AND booking.user_id=users.login_id AND booking.booking_id=booking_assign.booking_id AND booking_assign.tailor_id='"+str(tailorid)+"' and booking_assign.status='completed' and booking_assign.assign_date between '"+fromdate+"' and '"+todate+"'"
    res=db.select(qry)
    return render_template("tailor/view_previous_works.html",data=res)

@app.route("/view_profile")
def view_profile():
    tailorid=session['tailorid']
    db=Db()
    qry="SELECT * FROM tailor WHERE login_id='"+str(tailorid)+"'"
    res=db.selectOne(qry)
    return render_template("tailor/view_profile.html",data=res)


@app.route("/logout")
def logout():
    return render_template("login.html")

@app.route("/a")
def a():
    return render_template("admin/index.html")





#############################################               ANDROID METHODS
@app.route('/and_login', methods=['post'])
def and_login():
    db=Db()
    username=request.form['uname']
    password=request.form['pswd']
    qry="SELECT * FROM login WHERE username='"+username+"' AND PASSWORD='"+password+"'"
    res=db.selectOne(qry)
    if res is None:
        return jsonify(status="no")
    else:
        type=res['type']
        if type=="user":
            print('ok')
            return jsonify(status="ok",lid=res['login_id'])
        else:
            return jsonify(status="no")

@app.route("/and_signup", methods=['post'])
def and_signup():
    name=request.form['name']
    gender=request.form['gender']
    email=request.form['email']
    image=request.files['image']
    phone=request.form['phone']
    house=request.form['house']
    post=request.form['post']
    city=request.form['city']
    pin=request.form['pin']
    password=request.form['password']

    import time
    dt=time.strftime("%Y%m%d_%H%M%S")
    image.save(static_path + "user_image\\" + dt+".jpg")
    path = "/static/user_image/" +  dt+".jpg"
    qry="insert into login(`username`,`password`,`type`)values('"+email+"','"+password+"','user')"
    db=Db()
    lid=db.insert(qry)
    qry1="INSERT INTO users(NAME,gender,email,phone,house,post,city,pin,image,login_id)VALUES('"+name+"','"+gender+"','"+email+"','"+phone+"','"+house+"','"+post+"','"+city+"','"+pin+"','"+path+"','"+str(lid)+"')"
    db.insert(qry1)
    return jsonify(status="ok")

@app.route("/and_view_profile",methods=['post'])
def and_view_profile():
    lid=request.form['lid']
    qry="SELECT * FROM users WHERE login_id='"+lid+"'"
    db=Db()
    res=db.selectOne(qry)
    return jsonify(status="ok", name=res['name'], gen=res['gender'], email=res['email'], phone=res['phone'], house=res['house'],post=res['post'],city=res['city'],pin=res['pin'],image=res['image'])

@app.route("/and_update_profile",methods=['post'])
def and_update_profile():
    name=request.form['name']
    gender=request.form['gender']
    phone=request.form['phone']
    house=request.form['house']
    post=request.form['post']
    city=request.form['city']
    pin=request.form['pin']
    lid=request.form['lid']
    email=request.form['email']
    db=Db()
    if 'image' in request.files:
        image = request.files['image']
        import time
        dt = time.strftime("%Y%m%d_%H%M%S")
        image.save(static_path + "user_image\\" + dt + ".jpg")
        path = "/static/user_image/" + dt + ".jpg"
        qry = "UPDATE users SET image='" + path + "' WHERE login_id='" + lid + "'"
        db.update(qry)
    qry="UPDATE users SET NAME='"+name+"',gender='"+gender+"',phone='"+phone+"',house='"+house+"',post='"+post+"',city='"+city+"',pin='"+pin+"',email='"+email+"' WHERE login_id='"+lid+"'"
    db.update(qry)
    return jsonify(status="ok")

@app.route("/and_change_passwordd",methods=['post'])
def and_change_passwordd():
    lid = request.form['lid']
    currentpassword=request.form['currentpassword']
    newpassword=request.form['newpassword']
    db=Db()
    qry="SELECT * FROM login WHERE PASSWORD='"+currentpassword+"' AND login_id='"+lid+"'"
    res=db.selectOne(qry)
    if res==None:
        return jsonify(status="no")
    else:
        qry2="UPDATE login SET PASSWORD='"+newpassword+"' WHERE login_id='"+lid+"'"
        db.update(qry2)
        return jsonify(status="ok")


@app.route("/and_view_measurement",methods=['post'])
def and_view_measurement():
    lid = request.form['lid']
    db=Db()
    qry="SELECT * FROM measurement WHERE user_id='"+lid+"'"
    res=db.selectOne(qry)
    m1 = res['m1']
    m2 = res['m2']
    m3 = res['m3']
    m4 = res['m4']
    m5 = res['m5']
    m6 = res['m6']
    m7 = res['m7']
    m8 = res['m8']
    m9 = res['m9']
    m10 = res['m10']
    ar=[]
    ar.append(m1)
    ar.append(m2)
    ar.append(m3)
    ar.append(m4)
    ar.append(m5)
    ar.append(m6)
    ar.append(m7)
    ar.append(m8)
    ar.append(m9)
    ar.append(m10)

    #           read data from csv
    import pandas as pd
    data=pd.read_csv(static_path+"size.csv")
    X=data.values[:,:10]
    Y=data.values[:,10]

    # load classifier
    rf=RandomForestClassifier()
    rf.fit(X, Y)

    #       predict size
    import numpy as np
    arr=np.array([ar])
    pred=rf.predict(arr)
    print(str(pred[0]))
    if str(pred[0])=="0.0":
        size="Small(S)"
    elif str(pred[0])=="1.0":
        size="Medium(M)"
    elif str(pred[0])=="2.0":
        size="Large(L)"
    elif str(pred[0])=="3.0":
        size="Extra Large(XL)"
    print("Predicted size : ",size)

    if res is not None:
        return jsonify(status="ok", size=size, m1=res['m1'], m2=res['m2'], m3=res['m3'], m4=res['m4'], m5=res['m5'], m6=res['m6'], m7=res['m7'], m8=res['m8'], m9=res['m9'], m10=res['m10'],)
    else:
        return jsonify(status="no")


@app.route("/and_send_complaint",methods=['post'])
def and_send_complaint():
    lid = request.form['lid']
    complaint=request.form['complaint']
    db=Db()
    qry="insert into complaint (date,user_id,complaint,reply,status)values(curdate(),'"+lid+"','"+complaint+"' ,'pending','pending')"
    db.insert(qry)
    return jsonify(status="ok")


@app.route("/and_view_complaint",methods=['post'])
def and_view_complaint():
    lid = request.form['lid']
    db=Db()
    qry="select * from complaint where user_id='"+lid+"'"
    res=db.select(qry)
    return jsonify(status="ok",data=res)



@app.route("/and_delete_complaint",methods=['post'])
def and_delete_complaint():
    complaintid=request.form['complaintid']
    db=Db()
    qry="delete from complaint where complaint_id='"+complaintid+"'"
    db.delete(qry)
    return jsonify(status="ok")


@app.route("/and_view_dress",methods=['post'])
def and_view_dress():
    db=Db()
    qry="select * from dress "
    res=db.select(qry)
    return jsonify(status="ok",data=res)


@app.route("/and_insert_order",methods=['post'])
def and_insert_order():
    lid=request.form["lid"]
    dressid=request.form["dress_id"]
    description=request.form["description"]
    count=request.form["count"]
    image=request.files['image']
    import time
    dt=time.strftime("%Y%m%d_%H%M%S")
    image.save(static_path + "booking\\" + dt+".jpg")
    path = "/static/booking/" +  dt+".jpg"
    expecteddate=request.form["expected_date"]
    db=Db()
    qry="insert into booking(date,user_id,dress_id,status,count,expected_date,description, image)values(curdate(),'"+lid+"','"+dressid+"','pending','"+count+"','"+expecteddate+"','"+description+"', '"+path+"')"
    res=db.insert(qry)
    return jsonify(status="ok")

@app.route("/and_delete_order",methods=['post'])
def and_delete_order():
    orderid=request.form['order_id']
    db=Db()
    qry="delete from booking where booking_id='"+orderid+"'"
    db.delete(qry)
    return jsonify(status="ok")

@app.route("/and_view_order_status",methods=['post'])
def and_view_order_status():
    lid=request.form['lid']
    db=Db()
    qry="SELECT booking.*,dress.name AS dress_name FROM dress, booking WHERE dress.dress_id=booking.dress_id AND booking.user_id='"+lid+"' and (booking.status='pending' or booking.status='assigned')"
    res=db.select(qry)
    return jsonify(status="ok",data=res)

@app.route("/and_view_previous_order",methods=['post'])
def and_view_previous_order():
    lid=request.form['lid']
    db=Db()
    qry="SELECT booking.*,dress.name AS dress_name FROM dress, booking WHERE dress.dress_id=booking.dress_id AND booking.user_id='"+lid+"' and booking.status='completed'"
    res=db.select(qry)
    print(qry)
    return jsonify(status="ok",data=res)


@app.route("/and_view_order_more",methods=['post'])
def and_view_order_more():
    orderid=request.form['orderid']
    db=Db()
    qry="SELECT booking.*,dress.name AS dress_name,tailor.name,tailor.email,tailor.phone,tailor.login_id FROM dress,tailor, booking,booking_assign WHERE dress.dress_id=booking.dress_id AND booking.booking_id='"+orderid+"' AND booking.booking_id=booking_assign.booking_id AND booking_assign.tailor_id=tailor.login_id"
    res=db.selectOne(qry)
    return jsonify(status="ok",date=res['date'],dressname=res['dress_name'],count=res['count'],expecteddate=res['expected_date'],
                   description=res['description'],bstatus=res['status'],name=res['name'],email=res['email'],phone=res['phone'],login_id=res['login_id'])


##########          android chat
@app.route("/in_message2",methods=['post'])
def in_message2():
    fromid=request.form['fromid']
    toid=request.form['toid']
    msg=request.form['msg']
    db=Db()
    qry="insert into chat(date, time, from_id, to_id, message) values(curdate(), curtime(), '"+fromid+"','"+toid+"','"+msg+"')"
    res=db.insert(qry)
    return jsonify(status="ok")

@app.route("/view_message2",methods=['post'])
def view_message2():
    fromid=request.form['fid']
    toid=request.form['toid']
    lmid=request.form['lastmsgid']
    db=Db()
    qry="select from_id, message as msg,date,time,chat_id from chat where chat_id>'"+lmid+"' AND ((to_id='"+toid+"' and  from_id='"+fromid+"') or (to_id='"+fromid+"' and from_id='"+toid+"')  )  order by chat_id asc"
    res=db.select(qry)
    return jsonify(status="ok", data=res)

def getdistance(x1,x2,y1,y2):

    a= max([x2,x1])- min([x2,x1])
    b= max([y2,y1])- min([y2,y1])

    d =sqrt((a*a)+(b*b))

    return d

######allllll
@app.route('/poseestimation',methods=['post'])
def poseestimation():

    heightofperson=float(request.form["height"])

    cid=request.form["cid"]

    image=request.files["pic"]
    imagepath = "D:\\project\\WEB\\fitme\\static\\" + "a.jpg"

    image.save(imagepath)

    import cv2

    # protoFile = "coco/openpose_pose_coco.prototxt.txt"
    # weightsFile = "coco/pose_iter_440000.caffemodel"
    protoFile = "D:\\project\\WEB\\fitme\\static\\openpose_pose_mpi_faster_4_stages.prototxt.txt"
    weightsFile = "D:\\project\\WEB\\fitme\\static\\pose_iter_160000.caffemodel"

    # Read the network into Memory
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    frame = cv2.imread(imagepath)

    h, w, c = frame.shape
    # Specify the input image dimensions
    inWidth = 368
    inHeight = 368
    # Prepare the frame to be fed to the network
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False)

    # Set the prepared object as the input blob of the network
    net.setInput(inpBlob)

    out=net.forward()
    H = out.shape[2]
    W = out.shape[3]

    # Empty list to store the detected keypoints
    #
    points = []

    #
    for i in range(16):
        # confidence map of corresponding body's part.
        probMap = out[0, i, :, :]
        # print(probMap)
    #
    # # Find global maxima of the probMap.
    #
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
    #
    # Scale the point to fit on the original image
        x = (w * point[0]) / W
        y = (h * point[1]) / H

        if prob > 0.6:
            cv2.circle(frame, (int(x), int(y)), 15, (0, 255, 255), thickness=-1)

            cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 2,
                    lineType=cv2.LINE_AA)

            points.append((i,int(x), int(y)))
    #
        else:

            cv2.circle(frame, (int(x), int(y)), 15, (0, 255, 255), thickness=-1)

            cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 2,
                        lineType=cv2.LINE_AA)

            points.append((i, int(x), int(y)))
            pass

            # points.append(None)


    cv2.imwrite("as_coco.jpg",frame)

    # return points,w,h

    totalpoints, w, h = points,w,h

    m = 0

    try:  # 0-13
        zeropoint = totalpoints[0]
        levenpoint = totalpoints[13]
        x1 = int(zeropoint[1])
        x2 = int(levenpoint[1])
        y1 = int(zeropoint[2])
        y2 = int(levenpoint[2])
        zerothirteen = getdistance(x1, x2, y1, y2)
        onepixelratio = zerothirteen / heightofperson
        # shouldersize
    except Exception as aa:
        print("errrrrr", aa)
        pass
    try:
        twopoint = totalpoints[2]
        fivepoint = totalpoints[5]
        x1 = int(twopoint[1])
        x2 = int(fivepoint[1])
        y1 = int(twopoint[2])
        y2 = int(fivepoint[2])
        two_five = getdistance(x1, x2, y1, y2)
        print("two five", two_five)
        # shouldersize
    except:
        pass
    try:
        twopoint = totalpoints[2]
        threepoint = totalpoints[3]
        x1 = int(twopoint[1])
        x2 = int(threepoint[1])
        y1 = int(twopoint[2])
        y2 = int(threepoint[2])
        two_three = getdistance(x1, x2, y1, y2)
    except:
        pass
    try:  # 3-4
        threepoint = totalpoints[3]
        fourpoint = totalpoints[4]
        x1 = int(threepoint[1])
        x2 = int(fourpoint[1])
        y1 = int(threepoint[2])
        y2 = int(fourpoint[2])
        threefour = getdistance(x1, x2, y1, y2)
        print("threefour", threefour)
    except:
        pass
    try:  # 5-6
        fivepoint = totalpoints[5]
        sixpoint = totalpoints[6]
        x1 = int(fivepoint[1])
        x2 = int(sixpoint[1])
        y1 = int(fivepoint[2])
        y2 = int(sixpoint[2])
        fivesix = getdistance(x1, x2, y1, y2)
        print("fivesix", fivesix)
    except:
        pass
    try:  # 6-7
        sixpoint = totalpoints[6]
        sevenpoint = totalpoints[7]
        x1 = int(sixpoint[1])
        x2 = int(sevenpoint[1])
        y1 = int(sixpoint[2])
        y2 = int(sevenpoint[2])
        six_seven = getdistance(x1, x2, y1, y2)
        print("six_seven", six_seven)
    except:
        pass

    try:  # 8-11
        eightpoint = totalpoints[8]
        levenpoint = totalpoints[11]
        x1 = int(eightpoint[1])
        x2 = int(levenpoint[1])
        y1 = int(eightpoint[2])
        y2 = int(levenpoint[2])
        eightlevenpoint = getdistance(x1, x2, y1, y2)
    except:
        pass
    try:  # 8-9
        eightpoint = totalpoints[8]
        levenpoint = totalpoints[9]
        x1 = int(eightpoint[1])
        x2 = int(levenpoint[1])
        y1 = int(eightpoint[2])
        y2 = int(levenpoint[2])
        eightnine = getdistance(x1, x2, y1, y2)
    except:
        pass
    try:  # 9-10
        eightpoint = totalpoints[9]
        levenpoint = totalpoints[10]
        x1 = int(eightpoint[1])
        x2 = int(levenpoint[1])
        y1 = int(eightpoint[2])
        y2 = int(levenpoint[2])
        nineleven = getdistance(x1, x2, y1, y2)
    except:
        pass
    try:  # 11-12
        eightpoint = totalpoints[11]
        levenpoint = totalpoints[12]
        x1 = int(eightpoint[1])
        x2 = int(levenpoint[1])
        y1 = int(eightpoint[2])
        y2 = int(levenpoint[2])
        leventwelve = getdistance(x1, x2, y1, y2)
    except:
        pass
    try:  # 12-13
        twelvepoint = totalpoints[12]
        thirteenpoint = totalpoints[13]
        x1 = int(twelvepoint[1])
        x2 = int(thirteenpoint[1])
        y1 = int(twelvepoint[2])
        y2 = int(thirteenpoint[2])
        twelvethirteen = getdistance(x1, x2, y1, y2)
    except:
        pass
    print("done")
    try:
        from DBConnection import Db
        qry="delete from measurement where user_id='"+str(cid)+"' "
        db = Db()
        db.delete(qry)
        s=(two_five / onepixelratio).real
        print(type(s),"aaaaaaaaaaaaaaa")
        print(s,"aaaaaaa")
        qry = "INSERT INTO `measurement` (`m1`,`m2`,`m3`,`m4`,`m5`,`m6`,`m7`,`m8`,`m9`,`m10`,`user_id`) VALUES ('" + str(
            (two_five / onepixelratio).real) + "','" + str((two_three / onepixelratio).real) + "','" + str(
            (threefour / onepixelratio).real) + "','" + str((fivesix / onepixelratio).real) + "','" + str(
            (six_seven / onepixelratio).real) + "','" + str((eightlevenpoint / onepixelratio).real) + "','" + str(
            (eightnine / onepixelratio).real) + "','" + str((nineleven / onepixelratio).real) + "','" + str(
            (leventwelve / onepixelratio).real) + "','" + str(
            (twelvethirteen / onepixelratio).real) + "','" + str(cid) + "')"

        print(qry)
        db.insert(qry)
        import os
        # os.remove("D:\\project\\WEB\\fitme\\as_coco.jpg")
    except:
        print("errrror")
        pass
    return jsonify(status='ok')

@app.route("/adf", methods=['post'])
def aa():
    return "helloooo"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
