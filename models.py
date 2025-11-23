from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class Mentor(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    dob=models.DateField()
    photo=models.CharField(max_length=500)
    gender=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    video=  models.CharField(max_length=500)

class Student(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    dob = models.DateField()
    photo = models.CharField(max_length=500)
    gender = models.CharField(max_length=100)
    college= models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    place = models.CharField(max_length=100)

class Complaint(models.Model):
    date= models.DateField()
    complaint= models.CharField(max_length=100)
    LOGIN= models.ForeignKey(Login,on_delete=models.CASCADE)
    type= models.CharField(max_length=100)
    reply= models.CharField(max_length=100)
    status= models.CharField(max_length=100)

class Review(models.Model):
    date= models.DateField()
    STUDENT= models.ForeignKey(Student,on_delete=models.CASCADE)
    MENTOR= models.ForeignKey(Mentor,on_delete=models.CASCADE)
    review= models.CharField(max_length=100)

class Subject(models.Model):
    name= models.CharField(max_length=100)
    MENTOR= models.ForeignKey(Mentor,on_delete=models.CASCADE)
    code= models.CharField(max_length=100)


class Prev_year_qp(models.Model):
    title= models.CharField(max_length=100)
    code= models.CharField(max_length=100)
    year= models.CharField(max_length=100)
    MENTOR = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    qp=  models.CharField(max_length=500)

class LiveClass(models.Model):
    MENTOR = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date= models.DateField()
    time=models.TimeField()

class Notes(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    MENTOR = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    note = models.CharField(max_length=500)


class Feedback(models.Model):
    date= models.DateField()
    STUDENT= models.ForeignKey(Student,on_delete=models.CASCADE)
    feedback= models.CharField(max_length=100)

class Doubts(models.Model):
    date= models.DateField()
    STUDENT= models.ForeignKey(Student,on_delete=models.CASCADE)
    SUBJECT= models.ForeignKey(Subject,on_delete=models.CASCADE)
    doubt= models.CharField(max_length=100)
    reply= models.CharField(max_length=100)

class Chat(models.Model):
    FROMID= models.ForeignKey(Login, on_delete=models.CASCADE,related_name='fromc')
    TOID= models.ForeignKey(Login, on_delete=models.CASCADE,related_name='toc')
    messege= models.CharField(max_length=100)
    date=models.DateField()

class GroupChat(models.Model):
    STUDENT= models.ForeignKey(Student, on_delete=models.CASCADE)
    messege= models.CharField(max_length=100)
    date=models.DateField()

