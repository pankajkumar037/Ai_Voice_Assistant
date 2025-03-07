import smtplib
from email.message import EmailMessage
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import re

def extract_email(input):
    # Regular expression pattern to match email addresses
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    
    # Search for email in the text
    match = re.search(email_pattern, input)
    
    # Return the email if found, else None
    return match.group(0) if match else None



def compose_email(input,google_api_key):

    prompt = f"""

    Input: {input}
    Output:
        -Do not write Subject on above of email here
        -my name is Pankaj Kumar,my email is pankajkumarjnv76653@gmailcom contact 0019902
        -generate  an  clear consise and crisp email to given output
        -Just give email no extra things
        
    """

    messages = [
        SystemMessage(content="You are an email writing assistant"),
        HumanMessage(content=prompt)
    ]

    llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            temperature=0.5, 
            max_tokens=100, 
            api_key=google_api_key
        )
    
    reponse=llm.invoke(messages)
    return reponse.content

def get_subject_of_email(input_text,google_api_key):
    prompt = PromptTemplate.from_template("Give me a good Subject for email about {input_text}. Just in  maximum 5 words")

    formatted_prompt = prompt.format(input_text=input_text)

    llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            temperature=0.5, 
            max_tokens=100, 
            api_key=google_api_key
        )
    
    response = llm.invoke(formatted_prompt)
    
    return response.content



# Step 1: Define Email Credentials
EMAIL_ADDRESS = "pk7372069@gmail.com"
EMAIL_PASSWORD = "sliet@37"

def send_email(user_input,api_key):
    try:
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = extract_email(user_input)
        msg['Subject'] = get_subject_of_email(user_input,api_key)
        msg.set_content(compose_email(user_input,api_key))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return "Email sent successfully!"
    
    except Exception as e:
        return f"Error sending email: {e}"
    
