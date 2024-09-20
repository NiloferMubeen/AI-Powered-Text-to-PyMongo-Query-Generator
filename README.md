# AI-Powered-Text-to-PyMongo-Query-Generator
## Overview
AI-Powered Text-to-PyMongo Query Generator is an application that transforms natural language inputs into PyMongo queries using advanced AI techniques. The tool leverages LangChain, Groq, Pandas, Streamlit, and PyMongo to create a seamless interface for querying MongoDB databases.

## Features
**1.Natural Language Processing:** Converts user-friendly text inputs into complex PyMongo queries.

**2.Integrated Tools:** Utilizes LangChain, Groq, Pandas, Streamlit, and PyMongo for efficient query generation and execution.

**3.User-Friendly Interface:** Streamlit-based interface for easy interaction and visualization.

## Tools Used
* LangChain: Provides the framework for natural language understanding and query generation.
* ChatGroq: Chat model from Chatgroq
* Pandas: Used for data manipulation and analysis.
* Streamlit: Facilitates the creation of the web-based user interface.
* PyMongo: Enables interaction with MongoDB databases.
* Model:"mixtral-8x7b-32768"

# How to set up ?

### 1.Installation
**Prerequisites**
* Python 3.10 or higher
* MongoDB (installed and running)
* Pip (Python package installer)
* Streamlit
* langchain_groq
  
### 2. Clone the Repository

`git clone https://github.com/NiloferMubeen/AI-Powered-Text-to-PyMongo-Query-Generator.git
cd AI-Powered-Text-to-PyMongo-Query-Generator`


### 3.Set Up a Virtual Environment

It's recommended to use a virtual environment to manage your project's dependencies.

`python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate``

### 4. Install Dependencies

`pip install -r requirements.txt`

### 5. Configuration
Before running the application, configure your MongoDB connection and AI model settings.

**MongoDB Connection**

`mongo_url = 'mongodb://localhost:27017/'`

**AI model**

To use the groq_api_key in your Python project, follow these steps:

* Obtain Your API Key:
1.Visit the Groq API website and sign up or log in to your account.
2.Navigate to the API section and generate a new API key.
3. Copy the API key to a secure location.

Ensure that the AI model files and necessary configurations are correctly set up.

## Usage

To start the application, run the following command in your command prompt:
```python
streamlit run app.py

[![Watch the video](https://raw.githubusercontent.com/NiloferMubeen/AI-Powered-Text-to-PyMongo-Query-Generator/main/assets/Query-PyMongo.jpg)](https://raw.githubusercontent.com/NiloferMubeen/AI-Powered-Text-to-PyMongo-Query-Generator/main/assets/streamlit-app-2024-09-19-20-09-32.mp4))



