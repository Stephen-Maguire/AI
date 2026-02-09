import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from functions.generate_content import generate_content
from config import MAX_ITERS

def main():
	#Loads dotenv, gets the api key and checks for errors
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	if api_key is None:
		raise RuntimeError("API Key Problems")
	
    #initiates a client variable
	client = genai.Client(api_key=api_key)
	
    #gets the variable from user input ready
	parser = argparse.ArgumentParser(description="Chatbot")
	parser.add_argument("user_prompt", type=str, help="User prompt")
	parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
	args = parser.parse_args()
	messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
	iterations = 0
	is_done = False
	while (iterations<MAX_ITERS) and (not is_done):
		messages, final_text = generate_content(client, messages, args.verbose)
		if final_text:
			print(final_text)
			is_done = True
		iterations+=1
	if iterations == MAX_ITERS:
		print("Maximum number of iterations reached without fulfilling result")
		sys.exit(1)

if __name__ == "__main__":

    main()
