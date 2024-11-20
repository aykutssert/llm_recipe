# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials, auth
# import os


# if not os.path.exists("firebaseJson.json"):
#     print("firebaseJson.json bulunamadı!")
    

# # Firebase admin yapılandırması
# if not firebase_admin._apps:
#     cred = credentials.Certificate("firebaseJson.json")
#     firebase_admin.initialize_app(cred)

# def login_user():
#     st.title("Login")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         try:
#             user = auth.sign_in_with_email_and_password(email, password)
#             st.success(f"Welcome back, {email}!")
#             return {"logged_in": True, "email": email}
#         except Exception as e:
#             st.error(f"Login failed: {e}")
#             return {"logged_in": False}
#     return {"logged_in": False}


import streamlit as st
import requests
from firebase_admin import credentials, auth, initialize_app
import firebase_admin
from streamlit_js_eval import streamlit_js_eval

# Firebase Admin başlat
if not firebase_admin._apps:
    cred = credentials.Certificate("firebaseJson.json")
    initialize_app(cred)

def login_user():
    st.title("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        



    if submit:
        login_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyCQQ1U_zD78frg10OACqi4el7LXqrFv5DI"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        try:
            # Firebase REST API'ye POST isteği
            response = requests.post(login_url, json=payload)
            response_data = response.json()
            
            if response.status_code == 200:
                # ID token ve email'i tarayıcıya saklama (localStorage)
                st.session_state["user"] = {
                    "idToken": response_data["idToken"],
                    "refreshToken": response_data["refreshToken"],
                    "email": response_data["email"]
                }
                st.session_state.logged_in = True  # Oturum durumunu değiştir
                st.session_state.user_email = response_data["email"]
                st.session_state.page = "main"  # Input sayfasına geçişi tetikle
                st.success(f"Login successful! Redirecting...")
                
                # return {"logged_in": True, "email": response_data["email"]}
                # JavaScript ile token'ı localStorage'da saklama
                st.components.v1.html(f"""
                    <script>
                        localStorage.setItem("idToken", "{response_data['idToken']}");
                        localStorage.setItem("email", "{response_data['email']}");
                    </script>
                """, height=0)

            else:
                st.error(f"Giriş başarısız: {response_data['error']['message']}")
                # return {"logged_in": False, "email": None}

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
            # return {"logged_in": False, "email": None}



if "user" not in st.session_state:
    st.session_state["user"] = None
    st.session_state.logged_in = False
    st.session_state.page = "login"
# LocalStorage'daki bilgileri kontrol et
st.components.v1.html("""
    <script>
        const idToken = localStorage.getItem("idToken");
        const email = localStorage.getItem("email");
        if (idToken && email) {
            const message = JSON.stringify({ idToken, email });
            window.parent.postMessage(message, "*");
        }
    </script>
""", height=0)

# LocalStorage bilgilerini Streamlit'e yükle
def load_session_from_local_storage():
    query_params = st.query_params  # Yeni yöntemle query parametrelerini alın
    message = query_params.get("message")
    print(message)
    if message:
        user_data = eval(message[0])  # Gelen veriyi çözümle
        if "idToken" in user_data and "email" in user_data:
            st.session_state["user"] = {
                "idToken": user_data["idToken"],
                "email": user_data["email"],
            }
            st.session_state.logged_in = True
            st.session_state.page = "main"

# Sayfa her yüklemede bu kontrolü yap
if st.session_state.get("user") is None:
    load_session_from_local_storage()


