import streamlit as st
from firebaseCfg import firebaseConfig
import firebase_admin
from firebase_admin import credentials, auth
import os


if not os.path.exists("firebaseJson.json"):
    print("firebaseJson.json bulunamadı!")
    

# Firebase admin yapılandırması
if not firebase_admin._apps:
    cred = credentials.Certificate("firebaseJson.json")
    firebase_admin.initialize_app(cred)


def register_user():
    st.title("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        try:
            auth.create_user(email=email, password=password)
            # TODO mail varsa already hatası basalım.
            st.success("Account created successfully! Redirecting to Login page...")
        except Exception as e:
            st.error(f"Error creating account: {e}")
