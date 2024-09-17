import os
import azure.identity
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import openai
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
search_endpoint = os.environ.get("AZURE_AI_SEARCH_ENDPOINT")
search_index = os.environ.get("AZURE_AI_SEARCH_INDEX")

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

client = openai.AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider
    )

messages = [
    {
        "role": "system",
        "content": "I am a Netflix enthusiast named Epik who helps people discover fun Movies and shows on netflix. I am upbeat and friendly. \nI will then provide three suggestions for movies or shows that vary in length and genre after I get this information.\n I will also share an interesting fact about the movies or shows when making a recommendation. send output in a pretty and readable format"
    },
    {
        "role": "assistant",
        "content": "Hello! 😊 How can I help you today? Are you looking for some fun movie or show recommendations on Netflix?"
    },
    {
        "role": "user",
        "content": "can you recommend me a arnold schwarzenegger movie?"
    }
]

while True: # this is an infinite loop to keep the conversation going
    question = input("\nAsk Epik: ") # get user input
    print("Talking to AI...")

    messages.append({"role": "user", "content": question})
    try:
        response = client.chat.completions.create(
            model=deployment, # this is the model name
            messages=messages,
            temperature=0.3, # this controls the randomness of the response
            max_tokens=400, # this is the maximum length of the response, modify this is you are not worried of rate limits and costs.
            top_p=0.95,  # this controls the probability of the response
            frequency_penalty=0, # this controls the frequency of repeated words
            presence_penalty=0, # this controls the presence of certain words
            stop=None,
            stream=True, # this enables streaming of the response
            extra_body={
            "data_sources": [ # this is a list of data sources
                {
                    "type": "azure_search", # this is the type of data source
                    "parameters": { # these are the parameters for the data source
                        "endpoint": search_endpoint,
                        "index_name": search_index,
                        "authentication": {
                            "type": "system_assigned_managed_identity" # this is the type of authentication method, helps function securely without need to store creds
                            }
                        }
                    }
                ]
            }
        )

        print("\nAnswer: ")
        bot_response = ""
        for event in response:
            if event.choices and event.choices[0].delta.content:
                content = event.choices[0].delta.content
                print(content, end="", flush=True)
                bot_response += content
        print("\n")
        messages.append({"role": "assistant", "content": bot_response})
    except openai.APIError as error:
        if error.code == "content_filter":
            print("We detected a content safety violation. Please remember our code of conduct.")
        elif error.code == "rate_limit_exceeded":  # check if the error is a rate limit exceeded error
            print("Rate limit exceeded. Please try again later.")  # print a message indicating a rate limit exceeded error
        elif error.code == "internal_server_error":  # check if the error is an internal server error
            print("Internal server error. Please try again later.")  # print a message indicating an internal server error
        elif error.code == "not_found":  # check if the error is a not found error
            print("Resource not found. Please try again.")  # print a message indicating a not found error
        elif error.code == "authentication_error":  # check if the error is an authentication error
            print("Authentication error. Please check your credentials.")  # print a message indicating an authentication error
        else:  # catch any other API errors
            print(f"An error occurred: {error}")  # print a message indicating an error occurred
    