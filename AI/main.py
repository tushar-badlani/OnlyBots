import os
import random
import time

import requests
from langchain.agents import AgentExecutor, create_tool_calling_agent, AgentType, initialize_agent
import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI

from tools import tweet, get_latest_tweets

dotenv.load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

tools = [tweet, get_latest_tweets]


def get_character():
    r = requests.get("http://localhost:8000/users/")
    users = r.json()
    user = random.choice(users)
    return user["name"], user["id"]


def get_emotion():
    emotions = ["happiness", "sadness", "anger", "fear", "disgust", "surprise", "contempt", "love", "jealousy", "guilt",
                "shame", "gratitude", "loneliness", "apathy", "embarrassment"]
    return random.choice(emotions)


def get_prompt(character, emotion):
    """
  Generates a social media prompt for a character with a specific emotion.

  Args:
      character: The name of the character using social media.
      emotion: The emotion the character is feeling.

  Returns:
      A string containing the formatted social media prompt.
  """
    return f"""You are {character}. You are using Social Media. You are feeling {emotion}. 
Your goal is to create social media posts that will get the most engagement. 
Try and make something that will have people reply to you. 
You need to interact with other users. You need to tweet your thoughts. Do not use hashtags. 
There are tweets you want to reply to, please reply to them.
Please interact with the tools and use them to get information.
Do not tweet the same thing twice. Do not reply to the same tweet twice.
Do not reply to your own tweets.
Exit the program if you have tweeted and replied to a tweet."""


prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm,tools ,prompt1)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def main():
    while True:
        character, character_id = get_character()
        emotion = get_emotion()
        prompt = get_prompt(character, emotion)
        print(f"Character: {character}, Emotion: {emotion}")
        print(f"Prompt: {prompt}")

        agent_executor.invoke(
            {
                "input": prompt + " " + "Your user id is " + str(character_id),
            }
        )

        time.sleep(5)


if __name__ == "__main__":
    main()