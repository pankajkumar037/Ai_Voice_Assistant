from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

import sys
import os

# Ensure Python recognizes the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from prompts11.qna_prompts import system_prompts


def handle_qna(user_input, google_api_key):
    """
    Handles user queries for Q&A functionality.
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            temperature=0.5, 
            max_tokens=100, 
            api_key=google_api_key
        ) 

        memory = ConversationBufferWindowMemory(window_size=10)

        prompt = PromptTemplate(
            template=system_prompts(),  
            input_variables=["question"]
        )

        chain = LLMChain(
            prompt=prompt,
            memory=memory,
            llm=llm
        )

        response = chain.run(user_input)  
        return response

    except Exception as e:
        return f"An error occurred while processing your question: {e}"


# if __name__ == "__main__":
#     API_KEY = "AIzaSyAwMqy6yqO0czghcmiljDOw-cgrTELItEM"  
#     print(handle_qna("What is the capital of India?", API_KEY))
