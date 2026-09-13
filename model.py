from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import config
import time
import os
import json

def get_gemini_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=config.GOOGLE_API_KEY,
        temperature=0.7
    )
    
    prompt = PromptTemplate(
        input_variables=["message"],
        template="""
        You are an AI assistant helping with customer inquiries. 
        Analyze the following message and provide a helpful response.
        
        Customer message: {message}
        
        Respond in JSON format with the following keys:
        - summary: A brief summary of the customer's inquiry
        - sentiment: Detected sentiment (positive, neutral, negative)
        - response: Your helpful response to the customer
        
        JSON Response:
        """
    )
    
    return LLMChain(llm=llm, prompt=prompt)

def generate_response(message, model_type="gemini"):
    start_time = time.time()
    
    try:
        if model_type == "gemini":
            chain = get_gemini_chain()
            raw_response = chain.run(message=message)
            
            try:
                # Try to parse JSON response
                parsed_response = json.loads(raw_response)
                response_text = parsed_response.get("response", raw_response)
                summary = parsed_response.get("summary", "")
                sentiment = parsed_response.get("sentiment", "")
            except:
                # Fallback if response is not valid JSON
                response_text = raw_response
                summary = "Customer inquiry"
                sentiment = "neutral"
                
        elif model_type == "llama3":
            # Placeholder for Llama3 implementation
            response_text = f"Llama3 model response to: {message}"
            summary = "Llama3 processed inquiry"
            sentiment = "neutral"
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
            
        duration = round(time.time() - start_time, 2)
        
        return {
            "response": response_text,
            "summary": summary,
            "sentiment": sentiment,
            "duration": duration,
            "model": model_type
        }
        
    except Exception as e:
        raise Exception(f"Error generating response with {model_type}: {str(e)}")
