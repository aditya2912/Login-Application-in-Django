from django.shortcuts import render
from re import sub
from rest_framework.authtoken.models import Token
from django.utils.functional import SimpleLazyObject
from django.http import HttpResponseRedirect
from .forms import NameForm, UserData, UserDetailsForm, UserDetails
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base


# Create your views here.
def insertValuesIntoDatabase(username, password):
   engine = create_engine('sqlite:///UserDatabase.db')
   Base = declarative_base()
   Base.metadata.bind = engine
   DBSession = sessionmaker(bind=engine)
   session = DBSession()
   userData = UserData(username=username, password=password)
   session.add(userData)
   try:
      session.commit()
      print("Data inserted successfully")
   except IOError:
       print("Unable to save data")


         
    

def insertValuesIntoUserDetailsDatabase(name, residence, email, phoneNumber):
    userDetailsEngine = create_engine('sqlite:///UserDetailsDatabase.db')
    Base = declarative_base()
    Base.metadata.bind = userDetailsEngine
    DBSession = sessionmaker(bind= userDetailsEngine)
    session = DBSession()
    userDetails = UserDetails(name=name, residence=residence, email=email, phoneNumber=phoneNumber)
    session.add(userDetails)
    try:
        session.commit()
        print("Data inserted successfully")
    except IOError:
        print("unable to save data")

# Just to check whether data is actually being inserted or not
def readDataFromDataBase():
    engine = create_engine('sqlite:///UserDatabase.db')
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.query(UserData).all()
    user = session.query(UserData).first()
    print(user.username)
    print(user.password)

def readDataFromUserDetailsDatabase():
    engine = create_engine('sqlite:///UserDetailsDatabase.db')
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.query(UserDetails).all()
    user = session.query(UserDetails).first()
    print(user.name)
    print(user.residence)
    print(user.email)
    print(user.phoneNumber)



def hello(request):
    return render( request, "C:/pythonprograms/project1/projectapp/templates/hello.html", {})


def login(request):
     submitButton = request.POST.get("submit")
     username = ""
     password = ""
     if request.method == 'POST':
          form = NameForm(request.POST)
          if form.is_valid():
           username = form.cleaned_data.get("your_name")
           password = form.cleaned_data.get("password")
           insertValuesIntoDatabase(username, password)
           readDataFromDataBase()

     else:
         form = NameForm()

     return render(request, 'name.html', {"form" :form})


def registerPage(request):
     return render( request, "C:/pythonprograms/project1/projectapp/templates/register.html", {})

def loginPage(request):
    return render(request, "C:/pythonprograms/project1/projectapp/templates/login.html", {})

def registerUser(request):
         registerButton = request.POST.get("submit")
         username = ""
         password = ""

         if request.method == 'POST':
             form = NameForm(request.POST)
             if form.is_valid():
                 username = form.cleaned_data.get("username")
                 password = form.cleaned_data.get("password")
                 insertValuesIntoDatabase(username, password)
                 readDataFromDataBase()
         else:
             form = NameForm()

         return render(request, 'userRegistered.html', {"form" :form})

def userLogin(request):
     registerButton = 'POST'
     username = ""
     password = ""
     canUserLogIn = False

     if request.method == 'POST':
         form = NameForm(request.POST)
         if form.is_valid():
             username = form.cleaned_data.get("username")
             password = form.cleaned_data.get("password")
             request.session['username'] = username
             engine = create_engine('sqlite:///UserDatabase.db')
             conn = engine.connect()
             Base = declarative_base()
             Base.metadata.bind = engine
             DBSession = sessionmaker(bind=engine)
             session = DBSession()
             query = session.query(UserData).filter(UserData.username.in_([username]), UserData.password.in_([password]) )
             result = query.first()
             if result and request.session.has_key('username'):
                 request.session['username'] = username 
                 print("Login Successful")
                 return render(request, 'HomePage.html', {"form" : form})
             else:
                 print("Invalid Credentials")
                 return render(request, 'invalidCredentials.html', {})

     else:
         form = NameForm()



def enterUserDetails(request):
    submitButton = request.POST.get("submit")
    name = ""
    residence = ""
    email = ""
    phoneNumber = ""


    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            residence = form.cleaned_data.get("residence")
            email = form.cleaned_data.get("email")
            phoneNumber = form.cleaned_data.get("phoneNumber")
            insertValuesIntoUserDetailsDatabase(name, residence, email, phoneNumber)
            readDataFromUserDetailsDatabase()

        else:
            form = UserDetailsForm()

    return render(request, 'enterUserDetails.html', {"form" :form} )


def enterUserDetailsPage(request):
    return render(request, 'userLoggedIn.html', {})


def viewUserDetails(request):     
    form = UserDetailsForm(request.POST)
    if 'username' in request.session:
      sessionUsername = request.session['username'] 
      
    else: 
      sessionUserName = ""
    
    engine = create_engine('sqlite:///UserDetailsDatabase.db')
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    userRecord = session.query(UserDetails).filter(UserDetails.name == sessionUsername).first()
    
    return render(request, 'userDetails.html', {"username" : sessionUsername, "residence" : userRecord.residence, "email" : userRecord.email, "phoneNumber" : userRecord.phoneNumber})


def updateUserDetails(request):
    form = UserDetailsForm(request.POST)
    if 'username' in request.session:
      sessionUsername = request.session['username'] 
      
    else: 
      sessionUserName = ""
    
    engine = create_engine('sqlite:///UserDetailsDatabase.db')
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    userRecord = session.query(UserDetails).filter(UserDetails.name == sessionUsername).first()
    
    return render(request , 'updateUserDetails.html', {"name" : userRecord.name, "residence" : userRecord.residence, "email" : userRecord.email, "phoneNumber" : userRecord.phoneNumber})


def submitUpdatedUserDetails(request):
    updateButton = request.POST.get("submit")
    updatedName = ""
    updatedResidence = ""
    updatedEmail = ""
    updatedPhoneNumber = ""
    if 'username' in request.session:
      sessionUsername = request.session['username'] 
      
    else: 
      sessionUserName = ""
    
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            updatedName = form.cleaned_data.get("name")
            updatedResidence = form.cleaned_data.get("residence")
            updatedEmail = form.cleaned_data.get("email")
            updatedPhoneNumber = form.cleaned_data.get("phoneNumber")
            engine = create_engine('sqlite:///UserDetailsDatabase.db')
            Base = declarative_base()
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind = engine)
            DBSession.bind = engine
            session = DBSession()
            session.query(UserDetails).all()
            user = session.query(UserDetails).filter(UserDetails.name == sessionUsername).first()
            user.name = updatedName
            user.residence = updatedResidence
            user.email = updatedEmail
            user.phoneNumber = updatedPhoneNumber
            session.commit()
            request.session['username'] = updatedName
            print(user.name)
            print(user.residence)
        else:
            form = UserDetailsForm()     
        return render(request, 'HomePage.html', {})
            