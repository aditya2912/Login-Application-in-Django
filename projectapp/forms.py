from django import forms
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

class NameForm(forms.Form):
     username = forms.CharField(label='Your name', max_length=100, required=False)
     password = forms.CharField(label='Password', max_length=30)

class UserDetailsForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50, required=True)
    residence = forms.CharField(label='Residence', max_length=50)
    email = forms.CharField(label='Email', max_length=50)
    phoneNumber = forms.CharField(label='Phone Number', max_length=50)
    nameFormObject = relationship(NameForm)
    
    
    
class Rubrics(forms.Form):
    rubricTitle = forms.CharField(label='rubricTitle', max_length=50, required=True)
    criteria1 = forms.CharField(label='criteria1', max_length=50, required=True)
    criteria2 = forms.CharField(label='criteria2', max_length=50, required=True)
    criteria3 = forms.CharField(label='criteria3', max_length=50, required=True)
    criteria4 = forms.CharField(label='criteria4', max_length=50, required=True)
    description1 = forms.CharField(label='description1', max_length=50, required=True)
    description2 = forms.CharField(label='description2', max_length=50, required=True)
    description3 = forms.CharField(label='description3', max_length=50, required=True)
    description4 = forms.CharField(label='description4', max_length=50, required=True)
    

Base = declarative_base()

class UserData(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class UserDetails(Base):
    __tablename__ = 'userDetails'
    name = Column(String, nullable=False, primary_key=True)
    residence = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False)
    userName = Column(Integer, ForeignKey('user.username'))
    user = relationship(UserData)
    
class RubricDetails(Base):
    __tablename__ = 'rubrics'
    rubricTitle = Column(String, nullable=False)
    criteria1 = Column(String, nullable=True)
    criteria2 = Column(String, nullable=True)
    criteria3 = Column(String, nullable=True)
    criteria4 = Column(String, nullable=True)
    description1 = Column(String, nullable=True)
    description2 = Column(String, nullable=True)
    description3 = Column(String, nullable=True)
    description4 = Column(String, nullable=True)
    userName = Column(String, nullable=True, primary_key=True)


engine = create_engine('sqlite:///UserDatabase.db')
userDetailsEngine = create_engine('sqlite:///UserDetailsDatabase.db')
rubricsEngine = create_engine('sqlite:///RubricsDatabase.db')

Base.metadata.create_all(engine)
Base.metadata.create_all(userDetailsEngine)
Base.metadata.create_all(rubricsEngine)
