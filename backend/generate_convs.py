from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
import random 
import csv
import json
import re


REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

api_key = 'e7bFCX6QqNaR2LAV0ZT8zklGIfVzVLo3'
model = 'mistral-large-latest'
client = MistralClient(api_key=api_key)

properties = {
    1:"""
        - the <Opponent>’s argumentation is developed at the end of the conversation
        - the <Opponent>’s argumentation puts you at a disadvantage
        - The <Opponent> is attacking Your thesis directly
        - The <Opponent> attack is objective
    """,
    2:"""
        - The <Opponent>’ argumentation is developed at the end of the conversation
        - The <Opponent>’s argumentation put You at a disadvantage
        - The <Opponent> is attacking your thesis directly
        - The <Opponent>’s attack is not objective
    """,
    3:"""
        - The <Opponent>'s argumentation is developed at the end of the conversation
        - The <Opponent>'s argumentation puts You at a disadvantage
        - The <Opponent> is not attacking your thesis directly
        - You can use the <Opponent>'s statements against him
    """,
    4:"""
        - The <Opponent>'s argumentation is developed at the end of the conversation
        - The <Opponent>'s argumentation puts you at a disadvantage
        - The <Opponent>' is not attacking your thesis directly
        - You cannot use the <Opponent>'s statements against him
    """,
    5:"""
        - The <Opponent>'s argumentation is developed at the end of the conversation
        - The <Opponent>'s argumentation does not put you at a disadvantage
        - The foundations of the <Opponent>'s thesis are solid
        - The <Opponent>'s thesis consequences can be used against it
        - Associating the <Opponent>'s thesis with a recognized truth leads to a contradiction
    """,
    6:"""
        - The <Opponent>'s argumentation is developed at the end of the conversation
        - The <Opponent>'s argumentation does not put you at a disadvantage
        - the foundations of the <Opponent>'s thesis are solid
        - the <Opponent>'s thesis consequences can be used against it
        - associating the <Opponent>'s thesis with a recognized truth does not lead to a contradiction
    """,
    7:"""
        - the <Opponent>'s argumentation is developed at the end of the conversation
        - the <Opponent>'s argumentation does not put you at a disadvantage
        - the foundations of the <Opponent>'s thesis are solid
        - the <Opponent>'s thesis consequences cannot be used against it
        - the <Opponent> is not in a position of strength
    """,
    8:"""
        - the <Opponent>'s argumentation is developed at the end of the conversation
        - the <Opponent>'s argumentation does not put you at a disadvantage
        - the foundations of the <Opponent>'s thesis are solid
        - the <Opponent>'s thesis consequences cannot be used against it
        - the <Opponent> in not in a position of strength
    """,
    9:"""
        - the <Opponent>'s argumentation is developed at the end of the conversation
        - the <Opponent>'s argumentation des not put you at a disadvantage
        - the foundations of the <Opponent>'s thesis are not solid
        - you can demonstrate that the foundations of the <Opponent>'s thesis are false
    """,
    10:"""
        - the <Opponent>'s argumentation is developed at the end of the conversation
        - the <Opponent>'s argumentation does not put you at a disadvantage
        - the foundations of the <Opponent>'s thesis are not solid
        - you cannot demonstrate that the foundations of the <Opponent>'s thesis are false
        - the <Opponent> is honest
    """,
    11:"""
        - the <Opponent>'s argumentation is developed at the end of the conversation
        - the <Opponent>'s argumentation does not put you at a disadvantage
        - the foundations of the <Opponent>'s thesis are not solid
        - you cannot demonstrate that the foundations of the <Opponent>'s thesis are false
        - the <Opponent> is not honest
    """,
    12:"""
        - the <Opponent>'s is not developed at the end of the conversation
        - the <Opponent>'s thesis is not clearly defined
    """,
    13:"""
        - the <Opponent>'s argumentation is not developed at the end of the conversation
        - the <Opponent>'s thesis is not clearly defined
        - the <Opponent>'s thesis contradicts his previous statements
    """,

    14:"""
        - the <Opponent>'s is not developed at the end of the conversation
        - the <Opponent>'s thesis is clearly defined
        - the <Opponent>'s thesis does not contradict his previous statements
    """,
}

conv_template = """
    You are generating a heated conversational debate on Twitter between two users, Opponent and You, on the topic of {topic}. 
    Messages should be short and in the style of tweets, that is to say direct, caustic, confrontational and snarky.   
    The generated debate should be such that your potential next response could be generated with the following assumptions about the discussion: {prop}.
    The conversation should be structured with the appropriate user tags to enclose each message, so each message from the Opponent should be enclosed between <Opponent> and <\Opponent> tags and each message from You should be enclosed between <You> and <\You> tags. 
    The debate consists of *exactly* {n_turns} turns, always starting with the <Opponent>.

    Here is a template of the debate structured output for exactly 3 tweets:

    Tweet 1:
    <Opponent> message from Opponent </Opponent>

    Tweet 2:
    <You> message from you </You>

    Tweet 3:
    <Opponent> message from Opponent </Opponent>

    Generate a conversation strictly following this output structure, and nothing more.
"""

topics = [
    "Regulatory failure vs. bank mismanagement: Was the Silicon Valley Bank collapse primarily due to regulatory failures or the bank's own mismanagement and risk-taking?",
    "The role of the Federal Reserve in the collapse: Should the Federal Reserve be held accountable for its light-touch approach to bank regulation, which contributed to the collapse of Silicon Valley Bank?",
    "The impact of deregulation on bank oversight: Did the 2019 changes to banking regulations, which exempted smaller banks from stricter scrutiny, contribute to the collapse of Silicon Valley Bank?",
    "The responsibility of the San Francisco Federal Reserve: Should the San Francisco Federal Reserve be held accountable for its failed supervision and misplaced priorities that enabled the collapse of Silicon Valley Bank?",
    "The role of interest rates and economic climate: To what extent did rising interest rates and a tough economic climate contribute to the Silicon Valley Bank collapse, and how can banks and regulators mitigate the impact of these factors on financial stability?",
    "The accountability of Silicon Valley Bank's management: Should Silicon Valley Bank's management be held accountable for the bank's collapse, or were they victims of circumstances beyond their control?",
    "The need for stricter bank oversight: Should banks be subject to stricter oversight and regulation to prevent similar collapses in the future, or would this stifle innovation and economic growth?",
    "The impact of social media on bank runs: To what extent did social media contribute to the rapid spread of information and panic that fueled the Silicon Valley Bank run, and how can regulators mitigate this risk in the future?",
    "The role of uninsured deposits in the collapse: Did the large share of uninsured deposits at Silicon Valley Bank contribute to the bank's collapse, and what measures can be taken to address this risk in the future?",
    "The broader implications for the financial system: What lessons can be learned from the Silicon Valley Bank collapse, and how can the financial system be strengthened to prevent similar crises in the future?",
]

all_convs = {}
for i in range(1000):
    prop = random.choice(list(properties.values()))
    print(prop)
    n_turns = random.randrange(1, 5, 2)
    print(f"Generating {n_turns} turns")
    topic = random.choice(topics)
    print(topic)
    # Temperature?
    chat_conv= client.chat(
        model=model,
        messages=[ChatMessage(
            role='user', 
            content=conv_template.format(topic=topic, prop=prop, n_turns=n_turns))
        ]
    )
    conv = chat_conv.choices[0].message.content
    all_convs[i] = re.sub(r'Tweet \d+:\n', "", conv).replace("\n\n", "")
    print(conv)
    print("---")

# Write convs
with open("all_convs.json",'w') as f:
    json.dump(all_convs, f)

