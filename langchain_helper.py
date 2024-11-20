


from langchain_core.prompts import PromptTemplate


from langchain_openai import ChatOpenAI
from secret_key import OPENAI_API_KEY
import os
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# model_id ="mistralai/Mistral-7B-Instruct-v0.3"
# llm = HuggingFaceEndpoint(
#     repo_id=model_id,
#     max_new_tokens=512,
#     temperature=0.1,
#     huggingfacehub_api_token=HUGGINGFACE_TOKEN_KEY
# )
model = ChatOpenAI(model="gpt-4o")



def get_answer(question):
    template = """Question: {parametre}
    Answer: Let's think step by step."""
    prompt = PromptTemplate(template=template, input_variables=["parametre"])

    chain = prompt | model

    content = chain.invoke(question)

    return content.content
def get_image_answer(image_url):
    # Prompt ve model işlemleri
    response = model([image_url])
    return response.content



# if __name__ == "__main__":
#     question = "How to make a cake?"
#     print(get_answer(question))



