import streamlit as st
from login import login_user
from register import register_user
from main import generate_recipe

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None

# Register'dan Login'e yönlendirme kontrolü
# if st.session_state.get("redirect_to_login", False):
#     st.session_state.redirect_to_login = False
#     st.query_params()

# Sayfa yönlendirmesi için session_state'deki 'page' kullanılıyor
if "page" not in st.session_state:
    st.session_state.page = "login"  # Varsayılan sayfa 'login'

# Navigation Sidebar
option = st.sidebar.radio("Navigation", ["Login", "Register", "Generate Recipe"])

if option == "Login":
    st.session_state.page = "login"
elif option == "Register":
    st.session_state.page = "register"
elif option == "Generate Recipe":
    if st.session_state.logged_in:
        st.session_state.page = "main"
    else:
        st.warning("You need to log in to access this page!")
        st.session_state.page = "login"

if st.session_state.page == "login":
    # login_result = login_user()
    # if login_result and login_result["logged_in"]:
    #     st.session_state.logged_in = True
    #     st.session_state.user_email = login_result["email"]
    #     st.session_state.page = "main"  # Input sayfasına yönlendir
    login_user()

elif st.session_state.page == "register":
    register_user()

elif st.session_state.page == "main":
    if st.session_state.logged_in:
        st.success(f"Logged in as: {st.session_state.user_email}")
        generate_recipe(st.session_state.user_email)
    else:
        st.warning("You need to log in to generate recipes! Please log in or register.")

# Logout işlemi
if st.session_state.logged_in and st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.pop("user", None)
    st.session_state.page = "login"  # Kullanıcı logout olduğunda login sayfasına yönlendir
