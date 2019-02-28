from django.shortcuts import render
from re import sub
from rest_framework.authtoken.models import Token
from django.utils.functional import SimpleLazyObject
from django.http import HttpResponseRedirect
from .forms import NameForm, UserData, UserDetailsForm, UserDetails, RubricDetails, Rubrics
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base


# Create your views here.
def deleteUserNameAndPassword(userName):
    userDataEngine = create_engine('sqlite:///UserDatabase.db')
    conn = userDataEngine.connect()
    Base = declarative_base()
    Base.metadata.bind = userDataEngine
    DBSession = sessionmaker(bind = userDataEngine)
    session = sessionmaker(bind = userDataEngine)
    userData =    session.query(UserData).filter(UserData.username.in_([userName])).first()
    try:
        session.delete(userData)
        session.commit()
        return render(request, 'adminHomePage.html', {})
    except IOError:
        return render(request, 'invalidCredentials.html', {})
        
        

def insertRubricsIntoDatabase(rubricTitle, criteria1, criteria2, criteria3, criteria4, description1, description2, description3, description4, userName):
    engine = create_engine('sqlite:///RubricsDatabase.db')
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    rubricsData = RubricDetails(rubricTitle=rubricTitle, criteria1=criteria1, criteria2=criteria2,criteria3=criteria3, criteria4=criteria4,description1 = description1, description2 = description2, description3 = description3, description4 = description4, userName = userName)
    session.add(rubricsData)
    try:
        session.commit()
    except IOError:
        print("Unable to save data")
        
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
   except IOError:
       print("Unable to save data")

def insertValuesIntoUserDetailsDatabase(name, residence, email, phoneNumber, sessionUsername):
    
    userDetailsEngine = create_engine('sqlite:///UserDetailsDatabase.db')
    Base = declarative_base()
    Base.metadata.bind = userDetailsEngine
    DBSession = sessionmaker(bind= userDetailsEngine)
    session = DBSession()
    userDetails = UserDetails(name=name, residence=residence, email=email, phoneNumber=phoneNumber, userName = sessionUsername)
    session.add(userDetails)
    try:
        session.commit()
    except IOError:
        print("unable to save data")

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
         else:
             form = NameForm()

         return render(request, 'userRegistered.html', {"form" :form})

def userLogin(request):
     registerButton = 'POST'
     username = ""
     password = ""

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
             if username == "admin" and password == "admin":
                    return render(request, 'adminHomepage.html', {})
             elif result and request.session.has_key('username'):
                 request.session['username'] = username 
                 return render(request, 'HomePage.html', {"form" : form})
             else:
                 return render(request, 'invalidCredentials.html', {})

     else:
         form = NameForm()



def enterUserDetails(request):
    submitButton = request.POST.get("submit")
    name = ""
    residence = ""
    email = ""
    phoneNumber = ""
    sessionUsername = request.session['username']


    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            residence = form.cleaned_data.get("residence")
            email = form.cleaned_data.get("email")
            phoneNumber = form.cleaned_data.get("phoneNumber")
            insertValuesIntoUserDetailsDatabase(name, residence, email, phoneNumber, sessionUsername)

        else:
            form = UserDetailsForm()

    return render(request, 'HomePage.html', {"form" :form} )


def enterUserDetailsPage(request):
    return render(request, 'userLoggedIn.html', {})


def viewUserDetails(request):     
    form = UserDetailsForm(request.POST)
    if 'username' in request.session:
        sessionUsername = request.session['username']      
    else: 
        sessionUsername = ""
    engine = create_engine('sqlite:///UserDetailsDatabase.db')
    conn = engine.connect()
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    userRecord = session.query(UserDetails).filter(UserDetails.userName.in_([sessionUsername])).first()    
    
    return render(request, 'userDetails.html', {"username" : sessionUsername, "residence" : userRecord.residence, "email" : userRecord.email, "phoneNumber" : userRecord.phoneNumber})


def updateUserDetails(request):
    form = UserDetailsForm(request.POST)
    if 'username' in request.session:
        sessionUsername = request.session['username'] 
      
    else: 
        sessionUsername = ""
    
    engine = create_engine('sqlite:///UserDetailsDatabase.db')
    conn = engine.connect()
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    userRecord = session.query(UserDetails).filter(UserDetails.userName == sessionUsername).first()
    
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
        sessionUsername = ""
    
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
            user = session.query(UserDetails).filter(UserDetails.userName == sessionUsername).first()
            user.name = updatedName
            user.residence = updatedResidence
            user.email = updatedEmail
            user.phoneNumber = updatedPhoneNumber
            session.commit()
            print(user.name)
            print(user.residence)
        else:
            form = UserDetailsForm()     
        return render(request, 'HomePage.html', {})
            

def logOut(request):
    try:
        del request.session['username']
        return render(request, 'hello.html', {})
    except IOError:
        return render(request, 'invalidCredentials.html', {})
    
def rubricsForm(request):
    return render(request, 'rubrics.html', {})

def submitRubrics(request):
    rubricsForm = request.POST.get("submit")
    rubricTitle = ""
    criteria1 = ""
    criteria2 = ""
    criteria3 = ""
    criteria4 = ""
    description1 = ""
    description2 = ""
    description3 = ""
    description4 = ""
    username = request.session['username']
    if request.method == 'POST':
        form = Rubrics(request.POST)
        if form.is_valid():
            rubricTitle = form.cleaned_data.get("rubricTitle")
            criteria1 = form.cleaned_data.get("critera1")
            criteria2 = form.cleaned_data.get("critera2")
            criteria3 = form.cleaned_data.get("critera3")
            criteria4 = form.cleaned_data.get("critera4")
            description1 = form.cleaned_data.get("description1")
            description2 = form.cleaned_data.get("description2")
            description3 = form.cleaned_data.get("description3")
            description4 = form.cleaned_data.get("description4")
            try:
                insertRubricsIntoDatabase(rubricTitle, criteria1, criteria2, criteria3, criteria4, description1, description2, description3, description4, username)
                print("rubrics successfully Inserted")
                return render(request, 'HomePage.html', {"form" :form})
            except IOError:
                print("Error")
                return render(request, 'invalidCredentials.html', {})
        else:
            form = Rubrics()
            return render(request, 'invalidCredentials.html', {})
    
def viewRubricsForUser(request):
    userName = request.POST.get('userName', '')
    engine = create_engine('sqlite:///RubricsDatabase.db')
    conn = engine.connect()
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        rubricDetails =  session.query(RubricDetails).filter(RubricDetails.userName.in_([userName])).first()
        print("Value fetched successfully")
    except IOError:
        print("ERROR IN FETCHING RUBRIC DETAILS")
    
    return render(request, 'viewRubricDetails.html', {"rubricTitle" : rubricDetails.rubricTitle, "criteria1" : rubricDetails.criteria1, "criteria2" : rubricDetails.criteria2, "criteria3" : rubricDetails.criteria3, "criteria4" : rubricDetails.criteria4, "description1" : rubricDetails.description1, "description2" : rubricDetails.description2, "description3" : rubricDetails.description3, "description4" : rubricDetails.description4})

def adminLogOut(request):
    try:
        del request.session['username']
        return render(request, 'hello.html', {})
    except IOError:
        return render(request, 'invalidCredentials.html', {})
    
def deleteUser(request):
    userName = request.POST.get('userName', '')
    engine = create_engine('sqlite:///UserDetailsDatabase.db')
    conn = engine.connect()
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    userDetails = session.query(UserDetails).filter(UserDetails.userName.in_([userName])).first()
    if userDetails == None:
        userDataEngine = create_engine('sqlite:///UserDatabase.db')
        conn = userDataEngine.connect()
        Base = declarative_base()
        Base.metadata.bind = userDataEngine
        DBSession = sessionmaker(bind = userDataEngine)
        session = DBSession()
        userData =          session.query(UserData).filter(UserData.username.in_([userName])).first()
        session.delete(userData)
        session.commit()
        print("Successfully Deleted")
        return render(request, 'adminHomePage.html', {})
    else:
        userDetailsEngine = create_engine('sqlite:///UserDetailsDatabase.db')
        connection = userDetailsEngine.connect()
        Base = declarative_base()
        Base.metadata.bind = userDetailsEngine
        DBSession = sessionmaker(bind = userDetailsEngine)
        session = DBSession()
        userDetails =                      session.query(UserDetails).filter(UserDetails.userName.in_([userName])).first()
        try:
            session.delete(userDetails)
            session.commit()
            deleteUserNameAndPassword(userName)
            
        except IOError:
            return render(request, 'invalidCredentials.html', {s})