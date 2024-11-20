import streamlit as st
import base64
from langchain_helper import get_answer, get_image_answer
from langchain_core.messages import HumanMessage

def generate_recipe(email):
    st.title("Turkish Food Recipes")

    if "history" not in st.session_state:
        st.session_state.history = []

    if "ingredients" not in st.session_state:
        st.session_state.ingredients = ""
    if "widget" not in st.session_state:
        st.session_state.widget = ""

    def submit():
        st.session_state.ingredients = st.session_state.widget
        st.session_state.widget = ""

    st.text_input(
        "Enter the ingredients you have separated by commas",
        key="widget",
        on_change=submit,
    )

    text = st.session_state.ingredients
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if st.button("Generate Recipe"):
        if text:
            answer = get_answer(text)
            st.session_state.history.append({"ingredients": text, "recipe": answer})
            # db.child("history").child(email.replace(".", "_")).push(
            #     {"ingredients": text, "recipe": answer}
            # )
            st.write(f"**Generated Recipe:** {answer}")
        if uploaded_file:
            image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
            message = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": "What is the name of the historical building in this picture? Give information about the building.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ]
            )
            answer = get_image_answer(message)
            st.session_state.history.append({"ingredients": "image", "recipe": answer})
            # db.child("history").child(email.replace(".", "_")).push(
            #     {"ingredients": "image", "recipe": answer}
            # )
            st.write(f"**Generated Answer:** {answer}")

    # Display history
    if st.session_state.history:
        st.write("Recipe History:")
        for entry in st.session_state.history:
            st.write(f"**Input:** {entry['ingredients']}")
            st.write(f"**Recipe:** {entry['recipe']}")
            st.write("---")
    else:
        st.write("No recipe history available.")
