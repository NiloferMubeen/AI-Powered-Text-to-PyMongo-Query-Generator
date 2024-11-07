import os
import time
import base64
import pandas as pd
import streamlit as st
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_groq import ChatGroq

#------------------------------------ 1. LOADING THE CSV DATA TO MONGODB--------------------------------------------#

df = pd.read_csv("sample_data.csv")

df['LaunchDate'] = pd.to_datetime(df['LaunchDate'],format = "%d-%m-%Y")  # converting the datatype of the column to datetime

# Formatting the Percentage column

def remove_perc(x): # this function removes the '%' and typecasts to integer
    num = x.split("%")
    return int(num[0])

df['Discount'] = df['Discount'].apply(remove_perc)


# Establishing the connection with Mongodb and inserting all the documents

my_client = MongoClient("mongodb://localhost:27017/")
db = my_client["aiq"]

#db.Products.insert_many(df.to_dict('records'))  

# 2.---------------------------------------------STREAMLIT APPLICATION --------------------------------------------------#

st.set_page_config(page_title = 'Text to Pymongo Queries LLM',layout="wide")

# setting the background

def get_base64_of_bin_file(bin_file):
                with open(bin_file, 'rb') as f:
                    data = f.read()
                return base64.b64encode(data).decode()
            
def set_png_as_page_bg(png_file):
                    bin_str = get_base64_of_bin_file(png_file)
                    page_bg_img = '''
                                    <style>
                                    .stApp {
                                    background-image: url("data:image/png;base64,%s");
                                    background-size: cover;
                                    }
                                    </style>
                                    ''' % bin_str
                                                            
                    st.markdown(page_bg_img, unsafe_allow_html=True)
                    return
set_png_as_page_bg('img1.png') 
st.markdown("<h1 style='text-align: center; color:#581845 ;'>🍃 AI-Powered Text-to-PyMongo Query Generator</h1>", unsafe_allow_html=True)
st.divider()
c1,c2,c3 = st.columns([0.1,0.25,0.6])
with c2:
    st.image("mongo.png",width = 250)
with c3:
     
    question = st.text_input("Please Enter your question here")
    submit = st.button("Submit")


# 3.--------------------------------------------------  Dynamic Query Generation using LLM ---------------------------------#
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")  # Retrieves the value of the environment variable GROQ_API_KEY

# Instantiating the model 
llm = ChatGroq(  
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    
)
# Defining the Prompt
messages = [
    (
        "system",
        """You are a smart LLM capable of generating pymongo queries! The Mongodb database has the collection "Products" and 
        documents with the following fields, ProductID ,ProductName ,Category,Price,Rating,ReviewCount,Stock,Discount,Brand and LaunchDate.
        
        \n\n For example when you are asked queries as following,
                
        \n Example 1 - 'what are the unique ProductID?' The pymongo command would be 
                                    db.Products.distinct("ProductID"),
        \n Example 2 - 'what are is the average price of the products?' The pymongo command would be 
                                            
             db.Products.aggregate([{"$group": {"_id": None,"averagePrice": {"$avg": "$Price"}}}]) ;
                                            
        \n Example 3 - 'List the products that are in stock' the pymongo command should be 
                           'db.Products.find({"Stock": {"$gt": 0}})';
        \n Example 4 - 'List all the products launched after January,1,2022',the command should be
                            
                            db.Products.find({
                                    "LaunchDate": {
                                        "$gt": datetime(2022, 1, 1)
                                    }
                                });
                               
                         
        NO PREAMBLE OR EXPLANATION or quotes. 
        ## For aggregate commands do not create a separate pipeline,
        Generate command only for the question given"""),
    
    
    ("human", question)
]

ai_msg = llm.invoke(messages)

result = ai_msg.content

# ---------------------------------------------- Data Retrieval and Presentation----------------------------------------#
try:   
    if submit and result:
            documents = eval(result) 
            if documents:  
                
                st.dataframe(documents)  # Displays the data
            else:             # if no output is obtained, it would display Invalid
                st.error("Invalid question")
                
    else:
         pass
except:
    st.error("Results not found or Invalid question")        

# ---------------------------------------------- Save your file in CSV format----------------------------------------#    
try:
    if result :
        
        with c3:
            if st.button("Save"):
                documents = eval(result) 
                df1 = pd.DataFrame(documents)
                df1.to_csv("my_file.csv",index=False)
                with st.spinner("Saving file..."):
                        time.sleep(2)
                        st.success("File saved")
except:
    st.error("Please enter a query")
    
my_client.close() #closing the mongo db connection
        
