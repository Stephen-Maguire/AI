import copy
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def generate_content(client, messages, is_verbose):
    #initializes an object to check if we are done
    final_text = None

    #initializes the ai_response object, a GenerateContent object that we shall use
    ai_response = client.models.generate_content(model="gemini-2.5-flash", contents=messages,config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    
    #copies the messages object
    new_messages = copy.deepcopy(messages)

    #processes the candidate objects
    if ai_response.candidates:
        for candidate_ob in ai_response.candidates:
            if candidate_ob and candidate_ob.content:
                new_messages.append(candidate_ob.content)
    
    if not(ai_response.function_calls):
        final_text = ai_response.text or ""
        return new_messages, final_text

    #now we process function_calls
    else:
        function_results = []
        for call in ai_response.function_calls:
            function_call_result = call_function(call, verbose=is_verbose)
            
            #clauses to guard against faulty calls
            if len(function_call_result.parts)<=0:
                raise Exception("Error: Faulty function call.")
            if function_call_result.parts[0].function_response == None:
                raise Exception("Error: Flawed function response")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Error: Faulty response field of the function response")
            
            #at this point all objects are valid so append parts[0] to function results which
            #should be a function_response object.
            else:
                function_results.append(function_call_result.parts[0])
                if is_verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response['result']}")
        new_messages.append(types.Content(role="user", parts=function_results))
    return new_messages, final_text