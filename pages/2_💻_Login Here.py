import email
import pickle
from pathlib import Path
import streamlit as st
import pandas as pd
import pymongo
from pymongo import MongoClient
from streamlit_extras.switch_page_button import switch_page

CONNECTION_STRING = "localhost:27017"
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = pymongo.MongoClient(CONNECTION_STRING)

mydb = client['Patient']
information = mydb.Login

phydb = client['Physician']
information_phy = phydb.Login


# Security
#passlib,hashlib,bcrypt,scrypt
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

	menu = ["Patient", "Physician"]
	choice = st.selectbox("Login",menu)

	if choice == "Patient":
		st.subheader("Patient Login Form")
		with st.form(key="Login Form"):
			username = st.text_input("User Name")
			password = st.text_input("Password",type='password')
			st.text("Forgot Password?")
			st.write("")
			submit = st.form_submit_button(label="Submit")
			if submit == True:
				add_userdata ={
					'username' : username,
					'password': password
				}
				hashed_pwd = make_hashes(password)
				information.insert_one(add_userdata)
				st.success("You have successfully Logged in")
				switch_page("Analysis for patients")
				

	elif choice == "Physician":
		st.subheader("Login Section")
		st.subheader("Physician Login Form")
		with st.form(key="Login Form"):
			username = st.text_input("User Name")
			password = st.text_input("Password",type='password')
			submit = st.form_submit_button(label="Submit")
			if submit == True:
				add_phydata ={
					'username' : username,
					'password': password
				}
				# hashed_pwd = make_hashes(password)
				information_phy.insert_one(add_phydata)
				st.success("You have successfully Logged in")
				switch_page("Dashboard for Physicians")
				
if __name__ == '__main__':
	main()