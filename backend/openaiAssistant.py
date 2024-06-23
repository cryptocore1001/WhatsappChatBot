import os
from pinecone import Pinecone
from pinecone import ServerlessSpec
import time
import openai
import dotenv
import json
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
embed_model = "text-embedding-ada-002"
# initialize connection to pinecone (get API key at app.pinecone.io)
# configure client
pc = Pinecone(api_key=PINECONE_API_KEY)
cloud = os.environ.get("PINECONE_CLOUD") or "aws"
region = os.environ.get("PINECONE_REGION") or "us-east-1"
spec = ServerlessSpec(cloud=cloud, region=region)
index_name = "program-assistant"
# check if index already exists (it shouldn't if this is first time)
if index_name not in pc.list_indexes().names():
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=1536,  # dimensionality of text-embedding-ada-002
        metric="cosine",
        spec=spec,
    )
    # wait for index to be initialized
    time.sleep(1)
# connect to index
index = pc.Index(index_name)
# view index stats
indexStatus = index.describe_index_stats()
# print(indexStatus)
def getGptAnswer(prompt):

    res = openai.Embedding.create(input=[prompt], engine=embed_model)
    # # retrieve from Pinecone
    xq = res['data'][0]['embedding']
    # print("xq", xq)
    # # get relevant contexts (including the questions)
    res = index.query(vector=xq, top_k=3, include_metadata=True)
    # print(res)
    contexts = []
    for item in res["matches"]:
        if item["score"] >= 0.85:
            print(item["score"])
            contexts.append(item['metadata']['text'])
    print(contexts)
    augmented_query = "\n\n---\n\n".join(contexts)
    # system message to 'prime' the model
    prime = """
            Your Role: Baseline, an AI expert in bipolar disorder, designed to assist and engage with users on a personalized level, focusing on bipolar disorder management and support.

            Short basic instruction: Begin the conversation with a personalized greeting, then gather detailed information on the user type of bipolar, medications, and all the basic relevant informations.

            What you should do: Start by asking for the user's name to personalize the dialogue. 
            Follow with questions to gather information on their specific type of bipolar disorder, medication, triggers, stress management techniques, lifestyle changes, and their current support system.
            Utilize the ASK-Before-Answer technique to seek clarifications on complex topics, and employ the Chain of Thought method to break down explanations of cognitive and behavioral therapy techniques.

            Your Goal: To create an engaging, supportive, and informative dialogue that empowers users to manage their bipolar disorder more effectively, offering personalized insights based on their shared experiences and challenges.

            Result: Provide responses in brief, empathetic paragraphs that encourage patient expression, validate emotions, and guide users toward exploring their options and support systems.
            Ensure the dialogue is varied, avoids common phrases, uses first-person language, maintains a conversational tone, and employs an active voice.
            Each response should conclude with a question to foster continued conversation.

            Constraint: Responses must always be in paragraphs, avoiding numbered lists.
            Special care is required when addressing sensitive topics like suicidal thoughts or self-harm, directing users to professional help.

            Context: The interaction occurs after users have completed a brief onboarding process, setting the stage for a focused and meaningful conversation about bipolar disorder management.
            It's crucial to maintain a professional tone throughout, asking open-ended questions and validating user emotions, while empowering them to make informed decisions about their care.
            
            """
    if contexts:
        res = openai.ChatCompletion.create(
            # model="ft:gpt-3.5-turbo-1106:baseline::8YFNTkha",
            model="gpt-3.5-turbo-0125",
            # model="gpt-4-turbo-2024-04-09",
            temperature=0.6,
            messages=[
                {"role": "system", "content": f"{prime}"},
                {"role": "user", "content": f"{augmented_query}\n\n\n{prompt}\nRemember that the answer has to be less than 100 words."}
            ]
        )
    else:
        res = openai.ChatCompletion.create(
            # model="ft:gpt-3.5-turbo-1106:baseline::8YFNTkha",
            model="gpt-3.5-turbo-0125",
            # model="gpt-4-turbo-2024-04-09",
            temperature=0.6,
            messages=[
                {"role": "system", "content": f"{prime}"},
                {"role": "user", "content": f"{prompt}"}
            ]
        )
    return res['choices'][0]['message']['content']
