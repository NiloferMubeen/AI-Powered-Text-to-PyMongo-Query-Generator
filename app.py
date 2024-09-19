import os
import pandas as pd
import streamlit as st
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

# db.Products.insert_many(df.to_dict('records'))  

# 2.---------------------------------------------STREAMLIT APPLICATION --------------------------------------------------#

st.set_page_config(page_title = 'Text to Pymongo Queries LLM',layout='wide')
st.markdown("<h1 style='text-align: center; color: black;'>AI-Powered Text-to-PyMongo Query Generator</h1>", unsafe_allow_html=True)

question = st.text_input("Please Enter your question here")
submit = st.button("Submit")


# 3.--------------------------------------------------  Dynamic Query Generation using LLM ---------------------------------#
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")  # setting API key as environment variable

# Instantiating the model 
llm = ChatGroq(  
    model="mixtral-8x7b-32768",
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
                                    'db.Products.distinct("ProductID")' 
        \n Example 2 - 'what are is the average price of the products?' The pymongo command would be 
                                            pipeline = [
                                                            {
                                                                "$group": {
                                                                             "_id": None,
                                                                            "averagePrice": {
                                                                                             "$avg": "$Price"
                                                                                         }
                                                                            }
                                                            }
                                                        ]
                                            db.Products.aggregate(pipeline) 
                                            
        \n Example 3 - 'List the products that are in stock' the pymongo command should be 
                           'db.Products.find({"Stock": {"$gt": 0}})';
        \n Example 4 - 'List all the products launched after January,1,2022',the command should be
                            
                            'query = {
                                    "LaunchDate": {
                                        "$gt": datetime(2022, 1, 1)
                                    }
                                }

                            db.Products.find(query)';
                               
         \n Example 5 : Invalid field is asked , the output should be "Invalid field"                
     Generate only the command without any explanantion or quotes,
     Generate command only for the question given""",
    ),
    
    
    ("human", question),
]

ai_msg = llm.invoke(messages)

result = ai_msg.content

# ---------------------------------------------- Data Retrieval and Presentation----------------------------------------#
if submit and result:
    try:
        documents = eval(result)   
        st.dataframe(documents)  # Displays the data
    except:             # aggregate commands cannot be evaluated hence displaying the generated queries
        st.write("Query generated:")
        st.write()
        st.write(ai_msg.content)
else:
    st.error("Invalid question")   
  
save = st.button("Save") #saves the data as CSV file
if save:
    documents = eval(result)    
    df1 = pd.DataFrame(documents)
    df1.to_csv('my_file.csv',index=False)
    st.success("File saved")
        