# llm_handler.py
import pandas as pd
from pandasai import SmartDataframe
import pandasai
import os
import logging
from pandasai.llm import OpenAI
import base64

# pandasai.clear_cache()
# Configure Logging
logging.basicConfig(level=logging.INFO)

# Load and set up the data and environment
data = pd.read_csv("crime_data_california.csv")
os.environ['PANDASAI_API_KEY'] = ""
# openai_llm = OpenAI(
#     api_token="",
#     project_id="proj_DQgwPcqq1GkyCdkLnIDjoar4"
# )

# sdf = SmartDataframe(data,name="crime rate in california")
# sdf = SmartDataframe(data, name="crime rate in california",config={"enable_cache": False})
# df1 = SmartDataframe(data, name="crime rate sin california", config={"llm": openai_llm})

def get_response(prompt):
    sdf = SmartDataframe(data, name="crime rate in california",config={"enable_cache": False})
    try:
        response = sdf.chat(prompt)
        if isinstance(response, pd.DataFrame):
            # Convert DataFrame to JSON
            return response.to_json(orient='records'), 200, 'application/json'
        elif 'matplotlib' in str(type(response)):
            # Handle matplotlib figure (chart)
            img = BytesIO()
            response.savefig(img, format='png')
            img.seek(0)
            img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
            return img_base64, 200, 'image/png'
        elif 'int' in str(type(response)) or 'float' in str(type(response)):
            response=str(response)
            # Handle text response
            return response, 200, 'text/plain'
        else:
            # Handle text response
            return response, 200, 'text/plain'
    except TimeoutError:
        logging.error("Timeout error with LLM request.")
        return "Request timed out. Please try again later.", 504, 'text/plain'
    except ValueError as ve:
        logging.error(f"Value error: {ve}")
        return f"Data error: {ve}", 400, 'text/plain'
    except ConnectionError:
        logging.error("Connection error detected.")
        return "Failed to connect to the server. Please check your network.", 503, 'text/plain'
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}", 500, 'text/plain'
    
    sdf=None

# print(get_response("Which county had the highest rate of Robbery crime_type in 2006?"))
