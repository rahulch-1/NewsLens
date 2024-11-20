import os
import replicate
import envs

class ReplicateAPI:
    """
    High Level and Scalable API for accessing any model hosted on Replicate AI.
    """
    def __init__(self, model_name, api_token=envs.REPLICATE_API):
        os.environ['REPLICATE_API_TOKEN'] = api_token
        self.model_name = model_name
        self.input_params = {
            "top_k": 0,  
            "top_p": 0.9,  
            "prompt": "",  
            "max_tokens": 50,  
            "min_tokens": 0,  
            "temperature": 0.2,  
            "system_prompt": "You are a helpful assistant",  
            
            "prompt_template":  
                '''
                {prompt}
                Which of the following classes does the above statement fall into:
                1. Technology
                2. Sports
                3. Science
                4. Health
                ANSWER STRICTLY IN ONE WORD.
                ''',
            "presence_penalty": 1.15,  
            "log_performance_metrics": False  
        }

    def run_model(self, prompt) -> str:
        self.input_params['prompt'] = self.input_params['prompt_template'].format(prompt=prompt)

      
        try:
            out = replicate.run(self.model_name, input=self.input_params)
            
            categorized_output = out[0].strip() if out else "Unknown"
            
           
            valid_categories = ["Technology", "Sports", "Science", "Health"]
            if categorized_output in valid_categories:
                print(f"Your prompt was categorized under: {categorized_output}")
                return categorized_output
            else:
                print("Exiting program because no valid category was found for the prompt.")
                return "Unknown"
            
        except Exception as e:
            print("Error occurred:", str(e))
            return "Unknown"



if __name__ == '__main__':
    api = ReplicateAPI(model_name='meta/meta-llama-3-70b-instruct')
    
    output = api.run_model("cricket")
    print("Categorized output:", output)
















# import os
# import replicate
# import envs


# class ReplicateAPI:
#     """
#     High Level and Scalable API for accessing any model hostel on Replicate AI.
#     """
#     def __init__(self, model_name, api_token=envs.REPLICATE_API):
#         os.environ['REPLICATE_API_TOKEN'] = api_token
#         self.model_name = model_name
#         self.input_params = {
#             "top_p": 0.95,  # Probability threshold for generating the output.
#             "prompt": "",  # input prompt
#             "max_new_tokens": 3,  # Max. number of output tokens being generated.
#             "temperature": 0.2,  # Keep temperature low to avoid creativity (and hallucination)
#             "frequency_penalty": 1,  # Avoidance of repetition
#             "prompt_template":  # Prompt template
#                 '''
#                 <s>[INST] {prompt}
#                 ```ANSWER STRICTLY IN ONE WORD.  
#                 \nWhich of the following classes does the above statement fall into : 
#                 1. Technology\n 2. Sports\n 3. Science\n 4. Health\n
#                 [/INST] 
#                 '''
#         }

#     def run_model(self, prompt) -> list:
#         self.input_params['prompt'] = prompt
#         out = replicate.run(self.model_name, self.input_params)
#         return out


# if __name__ == '__main__':
#     api = ReplicateAPI(model_name='mistralai/mistral-7b-v0.1')
#     output = api.run_model("NASA Rocket Launch")
#     print(output)









# import os
# import replicate
# import envs

# class ReplicateAPI:
#     def __init__(self, model_name, api_token=envs.REPLICATE_API):
#         os.environ['REPLICATE_API_TOKEN'] = api_token
#         self.model_name = model_name
#         # Simplified parameters focused on getting a single category response
#         self.input_params = {
#             "max_new_tokens": 10,  # Short response needed
#             "temperature": 0.1,    # Low temperature for consistency
#             "top_p": 0.95,
#             "repetition_penalty": 1.0,
#             "prompt": None,        # Will be set in run_model
#         }

#     def run_model(self, prompt) -> str:
#         # Direct keyword mapping to ensure consistent categorization
#         term_mapping = {
#             "cricket": "Sports",
#             "football": "Sports",
#             "tennis": "Sports",
#             "medicine": "Health",
#             "computer": "Technology",
#             "internet": "Technology",
#             "biology": "Science",
#             "physics": "Science"
#         }
        
#         # Check for direct keyword match first
#         if prompt.lower() in term_mapping:
#             return term_mapping[prompt.lower()]
        
#         try:
#             # Construct prompt that guides a single-word response
#             instruction_prompt = f"""Based on this input: "{prompt}"

# You must choose exactly one category from these four options:
# - Technology (for tech, computers, digital topics)
# - Sports (for athletics, games, physical activities)
# - Science (for research, nature, discoveries)
# - Health (for medical, wellness topics)

# Respond with exactly one word - just the category name.
# Your response must be either: Technology, Sports, Science, or Health."""

#             self.input_params["prompt"] = instruction_prompt
            
#             # Run the model and get the response
#             output = replicate.run(
#                 self.model_name,
#                 input=self.input_params
#             )
            
#             # Convert output to list and get the first response
#             result = list(output)[0].strip()
            
#             # Debugging output
#             print(f"Model raw output: {result}")
            
#             # Validate the result
#             valid_categories = {"Technology", "Sports", "Science", "Health"}
#             result = result.capitalize()  # Ensure correct format
            
#             if result in valid_categories:
#                 return result
            
#             # Fallback keyword search if model output is unclear
#             prompt_lower = prompt.lower()
#             if any(sport in prompt_lower for sport in ["cricket", "football", "game", "sport", "play", "team", "athlete"]):
#                 return "Sports"
#             elif any(tech in prompt_lower for tech in ["computer", "digital", "software", "internet", "ai"]):
#                 return "Technology"
#             elif any(health in prompt_lower for health in ["medical", "disease", "doctor", "health"]):
#                 return "Health"
#             elif any(science in prompt_lower for science in ["research", "study", "science", "experiment"]):
#                 return "Science"
                
#             return "Science"  # Final fallback if nothing matches
            
#         except Exception as e:
#             print(f"Error occurred: {str(e)}")
#             return "Science"

# # Simple command-line interface for testing
# if __name__ == '__main__':
#     api = ReplicateAPI(model_name='meta/llama-2-70b-chat')
    
#     # Test specific cases
#     test_queries = [
#         "cricket",
#         "artificial intelligence",
#         "covid vaccine",
#         "space exploration",
#         "football match"
#     ]
    
#     print("\nTesting categorization:")
#     print("-" * 50)
#     for query in test_queries:
#         category = api.run_model(query)
#         print(f"Query: '{query}' -> Category: {category}")
#         print("-" * 50)
    
#     # Interactive testing
#     print("\nEnter your own queries:")
#     while True:
#         user_input = input("\nEnter your query (or 'quit' to exit): ")
#         if user_input.lower() == 'quit':
#             break
        
#         category = api.run_model(user_input)
#         print(f"Category: {category}")




# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from huggingface_hub import HfApi, login
# import torch

# # Your Hugging Face token
# hf_token = "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"

# # Authenticate using the token (only necessary once in a session)
# login(token=hf_token)

# # Load model and tokenizer with token authentication
# model_name = "mistralai/mixtral-8x7b-instruct-v0.1"
# tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
# model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=hf_token, torch_dtype=torch.float32)

# # Define the categorization pipeline
# categorization_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# # Define your target categories
# categories = ["Technology", "Science", "Health", "Sports"]

# def categorize_text(input_text, categories):
#     prompt = f"Classify the following text into one of the categories: {', '.join(categories)}.\nText: {input_text}\nCategory:"
#     result = categorization_pipeline(prompt, max_length=50, num_return_sequences=1, do_sample=False)
#     return result[0]["generated_text"].split("Category:")[1].strip()

# # Example input
# input_text = "New advances in AI are revolutionizing technology and science."

# # Run categorization
# category = categorize_text(input_text, categories)
# print(f"Predicted Category: {category}")
