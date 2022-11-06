# from msilib import add_data
from pathlib import Path
import streamlit as st
import pandas as pd
import pymongo
from pymongo import MongoClient
from streamlit_extras.switch_page_button import switch_page

# Security
#passlib,hashlib,bcrypt,scrypt
CONNECTION_STRING = "localhost:27017"
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = pymongo.MongoClient(CONNECTION_STRING)

mydb = client['Patient']
information = mydb.Register

phydb = client['Physician']
information_phy = phydb.Register


import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def main():
	"""Clinical Decision Support System for Migraine"""

	st.title("CLINICAL DECISION SUPPORT SYSTEM FOR MIGRAINE")
	st.title("REGISTRATION FORM")

	menu = ["Patient", "Physician"]
	choice = st.selectbox("Signup",menu)

	if choice == "Patient":
		st.subheader("Patient Registration Section")
		st.subheader("Create New Account")
		with st.form(key="Registration Form"):
			name = st.text_input("Name of the Patient")
			age = st.text_input("Age of the Patient")
			gender = st.text_input("Gender")
			username = st.text_input("Username")
			password = st.text_input("Password",type='password')
			submit = st.form_submit_button(label="Register")
			if submit == True:
				add_userdata ={
					'name' : name,
					'age' : age,
					'gender' : gender,
					'username' : username,
					'password': make_hashes(password)
				}
				# create_usertable()
				# add_userdata(new_user,make_hashes(new_password))
				information.insert_one(add_userdata)
				# add_userdata(username,make_hashes(password))
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")
				switch_page("login here")
		

	elif choice == "Physician":
		st.subheader("Physician Registration Section")
		st.subheader("Create New Account")
		with st.form(key="Registration Form"):
			name = st.text_input("Name of the Physician")
			username = st.text_input("Username")
			password = st.text_input("Password",type='password')
			submit = st.form_submit_button(label="Register")
			if submit == True:
				add_phydata ={
					'name' : name,
					'username' : username,
					'password': make_hashes(password)
					}
					# create_usertable()
					# add_userdata(new_user,make_hashes(new_password))
				information_phy.insert_one(add_phydata)
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")
				switch_page("login here")
				
		
	else:
		st.warning("Incorrect Username/Password")

if __name__ == '__main__':
	main()
