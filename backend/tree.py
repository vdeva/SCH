
debate_tree = {
    '0': {
        'question': 'Is the opponent\'s argumentation already developed?',
        'answers': {
            'yes': '1',
            'no': '7'
        }
    },
    '1': {
        'question': 'Does their argumentation put us at a disadvantage?',
        'answers': {
            'yes': '2',
            'no': '5'
        }
    },
    '2': {
        'question': 'Is the opponent attacking our thesis directly?',
        'answers': {
            'yes': '3',
            'no': '4'
        }
    },
    '3': {
        'question': 'Is the attack objective?',
        'answers': {
            'yes': '3a',
            'no': '3b'
        }
    },
    '3a': {
        'action': 'Begging the question',
    },
    '3b': {
        'action': 'Ad hominem argument',
    },
    '4': {
        'question': 'Can we use the opponent\'s statements against them?',
        'answers': {
            'yes': '4a',
            'no': '4b'
        }
    },
    '4a': {
        'action': 'Exploit contradictions',
    },
    '4b': {
        'action': 'Impudence to provoke the opponent',
    },
    '5': {
        'question': 'Are the foundations of the opponent\'s thesis solid?',
        'answers': {
            'yes': '5a',
            'no': '6'
        }
    },
    '5a': {
        'question': 'Can the thesis consequences be used against it?',
        'answers': {
            'yes': '5a1',
            'no': '5a2'
        }
    },
    '5a1': {
        'question': 'Does associating the thesis with a recognized truth lead to a contradiction?',
        'answers': {
            'yes': '5a1a',
            'no': '5a1b'
        }
    },
    '5a1a': {
        'action': 'Refutation by absurdity',
    },
    '5a1b': {
        'action': 'Find a contradictory example',
    },
    '5a2': {
        'question': 'Is the opponent in a position of strength?',
        'answers': {
            'yes': '5a2a',
            'no': '5a2b'
        }
    },
    '5a2a': {
        'action': 'Diversion',
    },
    '5a2b': {
        'action': 'Change of controversy',
    },
    '6': {
        'question': 'Can we demonstrate that the foundations are false?',
        'answers': {
            'yes': '6a',
            'no': '6b'
        }
    },
    '6a': {
        'action': 'Attack the foundations',
    },
    '6b': {
        'question': 'Honest or not?',
        'answers': {
            'yes': '6b1',
            'no': '6b2'
        }
    },
    '6b1': {
        'action': 'Strengthen the attack',
    },
    '6b2': {
        'action': 'Destabilize the opponent',
    },
    '7': {
        'question': 'Is the opponent\'s thesis clearly defined?',
        'answers': {
            'yes': '8',
            'no': '9'
        }
    },
    '8': {
        'question': 'Does the thesis contradict previous statements of the opponent (ad hominem)?',
        'answers': {
            'yes': '8a',
            'no': '8b'
        }
    },
    '8a': {
        'action': 'Ad hominem argument to highlight contradictions',
    },
    '8b': {
        'action': 'Explore consequences',
    },
    '9': {
        'action': 'Request clarifications',
    },
}

import random
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from dotenv import load_dotenv

load_dotenv(".env")

MISTRAL_API_TOKEN = os.getenv('MISTRAL_API_TOKEN')

model = 'mistral-large-latest'
client = MistralClient(api_key=MISTRAL_API_TOKEN)

history = """<Opponent> I firmly believe that Android is superior to Apple in every way. Android offers more customization options, a wider range of devices to choose from, and it's more affordable too. </Opponent>
<You> While it's true that Android does offer more customization and a wider range of devices, Apple's ecosystem is seamless and they offer top-notch customer service. Plus, Apple devices tend to have a longer lifespan. </You>
<Opponent> Well, that's where you're wrong. Android devices can last just as long with proper care. And as for customer service, Google's customer service is just as good, if not better. Plus, Android's open-source nature allows for more innovation and freedom. </Opponent>"""


a_prompt_template = """You are in a debate.

Here is the history of the debate you are in:
{history}

You are replying to your opponent. Use the strategy below:
{action}

Don't be polite. Be snarky.
"""


q_prompt_template = """You are in a debate.

Here is the history of the debate you are in:
{history}

You are analysing the opponent's arguments. Based on your analysis, answer the question below:
{question}

Only reply \"yes\" or \"no\". Do not answer anything else, do not describe your thoughts. Merely just answer \"yes\" or \"no\"."""

def get_ai_response(prompt):
    # Communicate with an AI model to get a response, simulated here.
    response = client.chat(
    model=model,
    messages=[ChatMessage(
        role='user', 
        content=prompt)
        ]
    )
    
    # Assume the response is expected to be 'yes' or 'no'.
    return (response.choices[0].message.content)

def q_response_parse(string):
    if 'yes' in string.lower():
        return 'yes'
    elif 'no' in string.lower():
        return 'no'
    return 'err'

def navigate_game_tree(tree, history, starting_node_id='0'):
    current_node = tree[starting_node_id]  # Start at the specified root node

    while 'question' in current_node:
        print(current_node['question'])  # Print the current question

        # Format the question with the history
        formatted_question = q_prompt_template.format(history=history, question=current_node['question'])
        
        # Get AI's response to the current question
        ai_answer = get_ai_response(formatted_question)
        print(f"AI's answer: {ai_answer}")

        # Move to the next node based on the AI's answer
        if q_response_parse(ai_answer) in current_node['answers']:
            next_node_id = current_node['answers'][q_response_parse(ai_answer)]
            current_node = tree[next_node_id]
        else:
            print("Error: AI provided an invalid response.")
            break

    # Once we reach an action node, print the action
    if 'action' in current_node:
        print("Action to take:", current_node['action'])
        # Format the action with the history
        formatted_action = a_prompt_template.format(history=history, action=current_node['action'])
        ai_action_response = get_ai_response(formatted_action)
        print(f"AI's action response: {ai_action_response}")

# Example usage of the function
navigate_game_tree(debate_tree, history)
