from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from myapp.models import *


def login(req):
    return render(req,'index.html')
def login_post(req):
    username=req.POST['username']
    password=req.POST['pass']
    lobj=Login.objects.filter(username=username,password=password)
    if lobj.exists():
        lobjj=Login.objects.get(username=username,password=password)
        req.session['lid']=lobjj.id
        if lobjj.type == "admin":
            return HttpResponse('''<script>alert("Login Successful");window.location='/myapp/home/'</script>''')
        elif lobjj.type == "mentor":
            return HttpResponse('''<script>alert("Login Successful");window.location='/myapp/home_mentor/'</script>''')
        else:
            return HttpResponse('''<script>alert("Login Unsuccessful");window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert("Invalid Username Or Password");window.location='/myapp/login/'</script>''')


def home(req):
    if req.session['lid']=="":
        return HttpResponse('''<script>alert("Session expired");window.location='/myapp/login/'</script>''')

    return render(req,'Admin/adminhome.html')

def mentorreg(req):
    if req.session['lid'] == "":
        return HttpResponse('''<script>alert("Session expired");window.location='/myapp/login/'</script>''')

    return render(req,'Admin/mentorreg.html')
def mentorreg_post(req):
    name=req.POST['textfield']
    email=req.POST['textfield2']
    dob = req.POST['textfield3']
    photo = req.FILES['photo']
    video = req.FILES['Video']
    gender = req.POST['RadioGroup1']
    phone = req.POST['textfield4']
    place = req.POST['textfield5']
    district = req.POST['textfield6']
    pin = req.POST['textfield7']
    qualification=req.POST['textfield8']


    from datetime import datetime
    date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"

    fs=FileSystemStorage()
    fs.save(date,photo)
    path=fs.url(date)

    date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".mp4"

    fs1 = FileSystemStorage()
    fs1.save(date1, video)
    path1 = fs1.url(date1)

    ll=Login()
    ll.username=email
    import random
    newpass=random.randint(0000,9999)
    ll.password=newpass
    ll.type='mentor'
    ll.save()

    mm=Mentor()
    mm.LOGIN=ll
    mm.name=name
    mm.email=email
    mm.dob=dob
    mm.photo=path
    mm.gender=gender
    mm.video=path1
    mm.phone=phone
    mm.place=place
    mm.district=district
    mm.pin=pin
    mm.qualification=qualification
    mm.save()

    return HttpResponse('''<script>alert("Registered Successfully");window.location='/myapp/mentorreg/'</script>''')



def mentorview(req):
    if req.session['lid'] == "":
        return HttpResponse('''<script>alert("Session expired");window.location='/myapp/login/'</script>''')
    res=Mentor.objects.all()
    return render(req,'Admin/mentorview.html',{'data':res})
def search_post(req):
    name=req.POST['search']
    res = Mentor.objects.filter(name__icontains=name)
    return render(req, 'Admin/mentorview.html', {'data': res})


def mentoredit(req,id):
    re=Mentor.objects.get(LOGIN_id=id)
    return render(req,'Admin/mentoredit.html',{'data':re})
def mentoredit_post(req):
    id=req.POST['id']
    name=req.POST['textfield']
    email=req.POST['textfield2']
    dob = req.POST['textfield3']

    gender = req.POST['RadioGroup1']
    phone = req.POST['textfield4']
    place = req.POST['textfield5']
    district = req.POST['textfield6']
    pin = req.POST['textfield7']
    qualification=req.POST['textfield8']






    ll=Login.objects.get(id=id)
    ll.username=email
    ll.save()

    mm=Mentor.objects.get(LOGIN_id=id)

    if 'photo' in req.FILES:
        photo = req.FILES['photo']
        if photo !="":
            from datetime import datetime
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"

            fs = FileSystemStorage()
            fs.save(date, photo)
            path = fs.url(date)
            mm.photo = path

    if 'Video' in req.FILES:
        video = req.FILES['Video']
        if video !="":
            from datetime import datetime

            date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".mp4"
            fs1 = FileSystemStorage()
            fs1.save(date1, video)
            path1 = fs1.url(date1)
            mm.video = path1


    mm.name=name
    mm.email=email
    mm.dob=dob
    mm.gender=gender

    mm.phone=phone
    mm.place=place
    mm.district=district
    mm.pin=pin
    mm.qualification=qualification
    mm.save()

    return HttpResponse('''<script>alert("Editted Succesfully");window.location='/myapp/mentorview/'</script>''')


def mentordelete(req,id):
    re=Mentor.objects.filter(LOGIN_id=id).delete()
    res=Login.objects.filter(id=id).delete()
    return redirect('/myapp/mentorview/')





def feedbackview(req):
    if req.session['lid'] == "":
        return HttpResponse('''<script>alert("Session expired");window.location='/myapp/login/'</script>''')
    res = Feedback.objects.all()
    return render(req,'Admin/feedbackview.html',{'data':res})

def feedbackview_post(req):
    fromdate = req.POST['fromdate']
    todate = req.POST['todate']
    res = Feedback.objects.filter(date__range=[fromdate,todate])
    return render(req,'Admin/feedbackview.html',{'data':res})


def changepasswd(req):
    if req.session['lid'] == "":
        return HttpResponse('''<script>alert("Session expired");window.location='/myapp/login/'</script>''')

    return render(req,'Admin/changepasswd.html')
def changepasswd_post(req):
    oldpassword = req.POST['textfield']
    newpassword = req.POST['textfield2']
    confirmpassword=req.POST['textfield3']
    lobj =Login.objects.filter(id=req.session['lid'], password=oldpassword)
    if lobj.exists():
        if newpassword == confirmpassword:
            Login.objects.filter(id=req.session['lid'], password=oldpassword).update(password=newpassword)
            return HttpResponse('''<script>alert("Password changed successfully");window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert("Password does not match");window.location='/myapp/changepasswd/'</script>''')
    else:
        return HttpResponse('''<script>alert("User Not Found");window.location='/myapp/changepasswd/'</script>''')


def complaintreply(req,id):
    return render(req,'Admin/complaintreply.html',{"data":id})

def complaintreply_post(req,):
    id=req.POST['cid']
    reply=req.POST['textarea']
    Complaint.objects.filter(id=id).update(reply=reply,status="Replied")
    return HttpResponse('''<script>alert("Replied Successfully");window.location='/myapp/complaintview/'</script>''')


def complaintview(req):
    if req.session['lid'] == "":
        return HttpResponse('''<script>alert("Session expired");window.location='/myapp/login/'</script>''')
    res = Complaint.objects.all()
    return render(req,'Admin/complaintview.html',{'data':res})

def complaintview_post(req):
    fromdate=req.POST['fromdate']
    todate=req.POST['todate']
    res = Complaint.objects.filter(date__range=[fromdate,todate])
    return render(req,'Admin/complaintview.html',{'data':res})






def studentview(req):
    if req.session['lid'] == "":
        return HttpResponse('''<script>alert("Session expired");window.location='/myapp/login/'</script>''')
    res = Student.objects.all()
    return render(req,'Admin/studentview.html',{'data':res})
def searchstud_post(req):
    name=req.POST['search']
    res = Student.objects.filter(name__icontains=name)
    return render(req, 'Admin/studentview.html', {'data': res})

def viewreview(req):
    if req.session['lid'] == "":
        return HttpResponse('''<script>alert("Session expired");window.location='/myapp/login/'</script>''')
    res = Review.objects.all()
    return render(req,'Admin/viewreview.html',{'data':res})

def viewreview_post(req):
    fromdate = req.POST['fromdate']
    todate = req.POST['todate']
    res = Review.objects.filter(date__range=[fromdate,todate])
    return render(req,'Admin/viewreview.html',{'data':res})



def logout(request):
    request.session['lid']=''
    return HttpResponse("<script>alert('logout');window.location='/myapp/login/'</script>")





################################################
def home_mentor(req):
    return render(req,'Mentor/Mentorhome.html')

def Viewprofile(req):
    re=Mentor.objects.get(LOGIN_id=req.session['lid'])
    return render(req,'Mentor/Viewprofile.html',{'data':re})

def Subjectview(req):


    data=Subject.objects.all()
    return render(req,'Mentor/Subjectview.html',{'data':data})

def Subjectview_post(req):
    return render(req,'Mentor/Subjectview.html')

def Viewpqp(req):
    data = Prev_year_qp.objects.all()
    return render(req,'Mentor/Viewpqp.html',{'data':data})
def Viewnotes(req):
    data = Notes.objects.all()
    return render(req,'Mentor/Viewnotes.html',{'data':data})
def Editsubject(req,id):
    data = Subject.objects.get(id=id)
    return render(req,'Mentor/Editsubject.html',{'data':data})


def EditSubjectpost(req):
    id = req.POST['id']
    name = req.POST['textfield']
    subcode = req.POST['textfield2']

    ss = Subject.objects.get(id=id)
    ss.name = name
    ss.code = subcode
    ss.save()

    return HttpResponse('''<script>alert("Updated Successfully");window.location='/myapp/Subjectview/'</script>''')


def Editpqp(req,id):
    data = Prev_year_qp.objects.get(id=id)
    return render(req,'Mentor/Editpqp.html',{'data':data})
def Editpqp_post(req):
    id = req.POST['id']
    name = req.POST['textfield']
    year = req.POST['textfield2']
    code = req.POST['textfield3']
    qp = req.FILES['fileField']

    ss = Prev_year_qp.objects.get(id=id)
    ss.title = name
    ss.code = code
    ss.year = year

    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"

    fs = FileSystemStorage()
    fs.save(date, qp)
    path = fs.url(date)
    ss.qp = path
    ss.save()
    return HttpResponse('''<script>alert("Updated Successfully");window.location='/myapp/Viewpqp/'</script>''')


def Editnotes(req,id):
    data=Notes.objects.get(id=id)
    return render(req,'Mentor/Editnotes.html',{'data':data})

def Editnotes_post(req):
    id = req.POST['id']
    name = req.POST['textfield']
    year = req.POST['textfield2']
    code = req.POST['textfield3']
    notes = req.FILES['fileField']

    ss = Notes.objects.get(id=id)
    ss.title = name
    ss.code = code
    ss.year = year

    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"

    fs = FileSystemStorage()
    fs.save(date, notes)
    path = fs.url(date)
    ss.note = path
    ss.save()
    return HttpResponse('''<script>alert("Added Successfully");window.location='/myapp/Viewnotes/'</script>''')


def Addsubject(req):
    return render(req,'Mentor/Addsubject.html')

def Addsubject_post(req):
    name=req.POST['textfield']
    subcode=req.POST['textfield2']

    ss=Subject()
    ss.MENTOR=Mentor.objects.get(LOGIN__id=req.session['lid'])
    ss.name=name
    ss.code=subcode
    ss.save()

    return HttpResponse('''<script>alert("added Successfully");window.location='/myapp/Addsubject/'</script>''')

def Addpqp(req):
    return render(req,'Mentor/Addpqp.html')

def Addpqp_post(req):
    name = req.POST['textfield']
    year = req.POST['textfield2']
    code = req.POST['textfield3']
    qp=req.FILES['fileField']

    ss = Prev_year_qp()
    ss.MENTOR = Mentor.objects.get(LOGIN__id=req.session['lid'])
    ss.title = name
    ss.code = code
    ss.year = year


    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"

    fs = FileSystemStorage()
    fs.save(date, qp)
    path = fs.url(date)
    ss.qp=path
    ss.save()
    return HttpResponse('''<script>alert("Added Successfully");window.location='/myapp/Addpqp/'</script>''')


def Addnotes(req):
    return render(req,'Mentor/Addnotes.html')
def Addnotes_post(req):
    name = req.POST['textfield']
    year = req.POST['textfield2']
    code = req.POST['textfield3']
    notes = req.FILES['fileField']

    ss = Notes()
    ss.MENTOR = Mentor.objects.get(LOGIN__id=req.session['lid'])
    ss.title = name
    ss.code = code
    ss.year = year

    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"

    fs = FileSystemStorage()
    fs.save(date, notes)
    path = fs.url(date)
    ss.note = path
    ss.save()
    return HttpResponse('''<script>alert("Added Successfully");window.location='/myapp/Addnotes/'</script>''')


def subjectdelete(req,id):
    re=Subject.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert("deleted Successfully");window.location='/myapp/Subjectview/'</script>''')

def pqpdelete(req,id):
    re=Prev_year_qp.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert("deleted Successfully");window.location='/myapp/Viewpqp/'</script>''')

def notesdelete(req,id):
    re=Notes.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert("deleted Successfully");window.location='/myapp/Viewnotes/'</script>''')

def doubtview(req):####
    res = Doubts.objects.all()
    return render(req,'Mentor/doubtview.html',{'data':res})
def doubtview_post(req):####
    fromdate=req.POST['fromdate']
    todate=req.POST['todate']
    res = Doubts.objects.filter(date__range=[fromdate,todate])
    return render(req,'Mentor/doubtview.html',{'data':res})

def doubtreply(req,id):####
    return render(req,'Mentor/doubtreply.html',{"data":id})

def doubtreply_post(req,):####
    id=req.POST['cid']
    reply=req.POST['textarea']
    Doubts.objects.filter(id=id).update(reply=reply)
    return HttpResponse('''<script>alert("Replied Successfully");window.location='/myapp/doubtview/'</script>''')

# def chat(req):
#     return render(req,'Mentor/chat.html')

def viewstudent(req):
    res = Student.objects.all()
    return render(req,'Mentor/viewstudent.html',{'data': res})
def viewstudent_post(req):
    name=req.POST['search']
    res = Student.objects.filter(name__icontains=name)
    return render(req,'Mentor/viewstudent.html',{'data': res})


#================Students=================================

def studentlogin(req):
    username=req.POST['username']
    password=req.POST['password']
    lobj = Login.objects.filter(username=username, password=password)

    if lobj.exists():
        lobjj = Login.objects.get(username=username, password=password)

        if lobjj.type == "student":
            lid=lobjj.id

            user = Student.objects.get(LOGIN_id=lid)

            return JsonResponse({'status':'ok','lid':str(lid),'name':user.name,'photo':user.photo})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})

def studentsignup(req):
    username=req.POST['username']
    email=req.POST['email']
    college=req.POST['college']
    gender=req.POST['gender']
    dob=req.POST['dob']
    place=req.POST['place']
    phone=req.POST['phone']
    photo=req.POST['photo']
    password=req.POST['password']


    import base64
    dt=datetime.now().strftime('%Y%m%d-%H%M%S')
    a=base64.b64decode(photo)
    fh=open("C:\\Users\\KRISHNAPRIYA\\PycharmProjects\\KTUstudymates\\media\\student\\"+dt+".jpg","wb")
    path='/media/student/'+dt+".jpg"
    fh.write(a)
    fh.close()


    l=Login()
    l.username=email
    l.password=password
    l.type="student"
    l.save()

    s=Student()
    s.name=username
    s.email=email
    s.dob=dob
    s.photo=path
    s.gender=gender
    s.college=college
    s.phone=phone
    s.place=place
    s.LOGIN=l
    s.save()


    return JsonResponse({'status': 'ok'})


def studentchangepassword(req):
    oldpassword = req.POST['oldpassword']
    newpassword = req.POST['newpassword']
    confirmpassword = req.POST['confirmpassword']
    lid = req.POST['lid']
    lobj = Login.objects.filter(id=lid, password=oldpassword)
    if lobj.exists():
        if newpassword == confirmpassword:
            Login.objects.filter(id=lid, password=oldpassword).update(password=newpassword)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})

def studentviewprofile(req):
    lid=req.POST['lid']
    data=Student.objects.get(LOGIN_id=lid)

    return JsonResponse({'status':'ok',
                         'name':data.name,
                         'email':data.email,
                         'dob':data.dob,
                         'photo':data.photo,
                         'gender':data.gender,
                         'college':data.college,
                         'phone':data.phone,
                         'place':data.place})


def studenteditprofile(req):
    username=req.POST['username']
    email=req.POST['email']
    college=req.POST['college']
    gender=req.POST['gender']
    dob=req.POST['dob']
    place=req.POST['place']
    phone=req.POST['phone']
    lid=req.POST['lid']
    s=Student.objects.get(LOGIN_id=lid)

    import base64
    photo=req.POST['photo']
    dt=datetime.now().strftime('%Y%m%d-%H%M%S')
    a=base64.b64decode(photo)
    fh=open("C:\\Users\\KRISHNAPRIYA\\PycharmProjects\\KTUstudymates\\media\\student\\"+dt+".jpg","wb")
    path='/media/student/'+dt+".jpg"
    fh.write(a)
    fh.close()

    s.name=username
    s.email=email
    s.dob=dob
    s.photo=path
    s.gender=gender
    s.college=college
    s.phone=phone
    s.place=place
    s.save()


    return JsonResponse({'status': 'ok'})



def studentviewtutor(req):
    data=Mentor.objects.all()
    l=[]
    for i in data:
        l.append({'id':i.id,

                  'name':i.name,
                  # 'email': i.email,
                  # 'dob': i.dob,
                  'photo': i.photo,
                  # 'gender': i.gnder,
                  # 'phone': i.phone,
                  # 'place': i.place,
                  # 'district': i.district,
                  # 'pin': i.pin,
                  'qualification': i.qualification,
                  'video': i.video,
                  'login_id':i.LOGIN.id
                  })
    print(l)
    return JsonResponse({'status':'ok','data':l})

def studentviewsubject(req):
    data=Subject.objects.all()
    l=[]
    for i in data:
        l.append({'name':i.name,
                  'mentor':i.MENTOR.id,
                  'code':i.code})
    return JsonResponse({'status':'ok','data':l})

def studentviewpqp(req):
    data=Prev_year_qp.objects.all()
    l=[]
    for i in data:
        l.append({'title': i.title,
                  'mentor': i.MENTOR.id,
                  'code': i.code,
                  'year': i.year,
                  'qp': i.qp,
                  })
    return JsonResponse({'status':'ok','data':l})

def studentviewnotes(req):
    data=Notes.objects.all()
    l=[]
    for i in data:
        l.append({'title': i.title,
                  'mentor': i.MENTOR.name,
                  'code': i.code,
                  'year': i.year,
                  'id': i.id,
                  'note': i.note,
                  })
    return JsonResponse({'status':'ok','data':l})

def studentchattutor(req):
    return JsonResponse({'status':'ok'})

def studentsendcomplaint(req):
    complaint=req.POST['complaint']
    lid=req.POST['lid']

    c=Complaint()
    c.date=datetime.now()
    c.complaint=complaint
    c.LOGIN_id=lid
    c.type='student'
    c.reply='pending'
    c.status='pending'
    c.save()

    return JsonResponse({'status':'ok'})

def studentviewcomplaintreply(req):
    lid=req.POST['lid']
    data=Complaint.objects.filter(LOGIN_id=lid)
    l = []
    for i in data:
        l.append({'date': i.date,
                  'LOGIN': i.LOGIN.id,
                  'complaint': i.complaint,
                  'type': i.type,
                  'reply': i.reply,
                  'status': i.status,
                  'id': i.id,
                  })
    return JsonResponse({'status':'ok','data':l})


def studentfeedback(req):
    lid=req.POST['lid']
    feedback = req.POST['feedback']

    f=Feedback()
    f.date=datetime.now()
    f.feedback=feedback
    f.STUDENT=Student.objects.get(LOGIN_id=lid)
    f.save()
    return JsonResponse({'status':'ok'})


def studentmentorreview(req):
    data = Review.objects.all()
    l = []
    for i in data:
        l.append({'date': i.date,
                  'STUDENT': i.STUDENT.id,
                  'MENTOR': i.MENTOR.id,
                  'review': i.review,
                  })
    return JsonResponse({'status':'ok','data':l})


def studentmentorGD(req):
    return JsonResponse({'status':'ok'})


def studentsubjectdoubts(req):
    lid=req.POST['lid']
    doubt=req.POST['doubt']
    reply=req.POST['reply']
    subject=req.POST['subject']

    d=Doubts()
    d.date=datetime.now()
    d.doubt=doubt
    d.reply=reply
    d.STUDENT = Student.objects.get(LOGIN_id=lid)
    d.SUBJECT_id=subject

    return JsonResponse({'status':'ok'})


def studentviewdoubtsreply(req):
    data = Doubts.objects.all()
    l = []
    for i in data:
        l.append({'date': i.date,
                  'STUDENT': i.STUDENT.id,
                  'SUBJECT': i.SUBJECT.id,
                  'doubt': i.doubt,
                  'reply': i.reply,
                  })
    return JsonResponse({'status':'ok','data':l})


def chat1(request,id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = Student.objects.get(LOGIN=cid)

    return render(request, "Mentor/Chat.html", {'photo': qry.photo, 'name': qry.name, 'toid': cid})

def chat_view(request):
    fromid = request.session["lid"]
    toid = request.session["userid"]
    qry = Student.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.messege, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id})

    return JsonResponse({'photo': qry.photo, "data": l, 'name': qry.name, 'toid': request.session["userid"]})

def chat_send(request, msg):
    lid = request.session["lid"]
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.messege = message
    chatobt.TOID_id = toid
    chatobt.FROMID_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})


#
# def chat1(request, id):
#     if request.session['lid']!='':
#         request.session["userid"] = id
#         cid = str(request.session["userid"])
#         request.session["new"] = cid
#         qry = Tailor.objects.get(login_id=cid)
#
#         return render(request, "user/user_chat.html", {'name': qry.username, 'toid': cid})
#     else:
#         return HttpResponse('''<script>alert('You are not Logined');window.location='/myapp/login/'</script>''')
#
#
# def chat_view1(request):
#     if request.session['lid']!='':
#         fromid = request.session["lid"]
#         toid = request.session["userid"]
#         qry = Tailor.objects.get(login=request.session["userid"])
#         from django.db.models import Q
#
#         res = Chat.objects.filter(Q(FROMID=fromid, TOID=toid) | Q(FROMID=toid, TOID=fromid))
#         l = []
#
#         for i in res:
#             l.append({"id": i.id, "message": i.message, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id})
#
#         return JsonResponse({'status':'ok', "data": l, 'name': qry.username, 'toid': request.session["userid"]})
#     else:
#         return HttpResponse('''<script>alert('You are not Logined');window.location='/myapp/login/'</script>''')
#
#
# def chat_send1(request, msg):
#     if request.session['lid']!='':
#         lid = request.session["lid"]
#         toid = request.session["userid"]
#         message = msg
#
#         import datetime
#         d = datetime.datetime.now().date()
#         chatobt = Chat()
#         chatobt.message = message
#         chatobt.TOID_id = toid
#         chatobt.FROMID_id = lid
#         chatobt.date = d
#         chatobt.save()
#     else:
#         return HttpResponse('''<script>alert('You are not Logined');window.location='/myapp/login/'</script>''')
#
#
#     return JsonResponse({"status": "ok"})
#
def studentsendreview(req):
    rev=req.POST['review']
    lid=req.POST['lid']
    mid=req.POST['mid']

    c=Review()
    c.date=datetime.now().today()
    c.review=rev
    c.STUDENT=Student.objects.get(LOGIN_id=lid)
    c.MENTOR_id=mid
    c.save()
    return JsonResponse({'status':'ok'})



def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROMID_id=FROM_id
    c.TOID_id=TOID_id
    c.messege=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.messege, "from": i.FROMID_id, "date": i.date, "to": i.TOID_id})

    return JsonResponse({"status":"ok",'data':l})

def User_sendGroupchat(request):
    STUDENT_id=request.POST['from_id']
    msg=request.POST['message']

    from  datetime import datetime
    c=GroupChat()
    c.STUDENT=Student.objects.get(LOGIN=STUDENT_id)
    c.messege=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def User_viewGroupchat(request):
    STUDENT_id = request.POST['from_id']
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = GroupChat.objects.all()
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.messege, "from": i.STUDENT.LOGIN.id, "date": i.date, "name": i.STUDENT.name})

    return JsonResponse({"status":"ok",'data':l})




from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

# Replace with your actual API key
GOOGLE_API_KEY = 'AIzaSyAaKvYDYAMj_jbpbvuiTOKhpBdQM10DaMI'
genai.configure(api_key=GOOGLE_API_KEY)

model = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
        model = genai.GenerativeModel('gemini-1.5-flash')
        break

def generate_gemini_response(prompt):
    # Directly use the user's question as the prompt
    response = model.generate_content(prompt)
    return response.text


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        user_message = json.loads(request.body).get('message')
        # Generate a response based on the user message without additional context
        gemini_response = generate_gemini_response(user_message)
        return JsonResponse({'response': gemini_response})