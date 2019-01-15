from django import forms
from sqlalchemy import Column, Integer, String
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


engine = create_engine('sqlite:///UserDatabase.db')
userDetailsEngine = create_engine('sqlite:///UserDetailsDatabase.db')

Base.metadata.create_all(engine)
Base.metadata.create_all(userDetailsEngine)
