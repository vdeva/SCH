
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
import replicate
import os
from dotenv import load_dotenv

load_dotenv(".env")

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')


prompt_template = """You are in a debate.

Here is the history of the debate you are in:
<Opponent>Working from home diminishes collaboration and spontaneity among team members, which is crucial for creative projects. People need direct interaction to spark innovative ideas.</Opponent>
<You>While face-to-face interaction is valuable, remote work offers flexibility and a better work-life balance. Many modern communication tools effectively bridge the gap in collaboration, allowing creativity to flourish in different ways.</You>
<Opponent>The problem with remote work is that it can lead to isolation and a disconnect from the company's culture. Employees might feel less engaged or loyal to the organization.</Opponent>
<You>Remote work, when managed well, can actually increase employee retention by addressing their needs for flexibility and autonomy. Companies can foster culture through regular virtual meetings and team-building activities.</You>
<Opponent>But monitoring productivity is much harder when employees are scattered across various locations. There's a risk of decreased accountability and performance.</Opponent>

You are analysing the opponent's arguments. Based on your analysis, answer the question below:
{question}

Only reply \"yes\" or \"no\". Do not answer anything else, do not describe your thoughts. Merely just answer \"yes\" or \"no\"."""

def get_ai_response(question):
    # Format the question using the prompt template
    formatted_question = prompt_template.format(question=question)
    
    # Communicate with an AI model to get a yes/no response, simulated here.
    response = replicate.run("meta/meta-llama-3-70b-instruct",
                             input={
                                "prompt": formatted_question,
                                "temperature": 2},)
    
    # Assume the response is expected to be 'yes' or 'no'.
    return ''.join(response)

def navigate_game_tree(tree, starting_node_id='0'):
    current_node = tree[starting_node_id]  # Start at the specified root node

    while 'question' in current_node:
        print(current_node['question'])  # Print the current question

        # Get AI's response to the current question
        ai_answer = get_ai_response(current_node['question'])
        print(f"AI's answer: {ai_answer}")

        # Move to the next node based on the AI's answer
        if ai_answer.lower() in current_node['answers']:
            next_node_id = current_node['answers'][ai_answer.lower()]
            current_node = tree[next_node_id]
        else:
            print("Error: AI provided an invalid response.")
            break

    # Once we reach an action node, print the action
    if 'action' in current_node:
        print("Action to take:", current_node['action'])

# Example usage of the function
navigate_game_tree(debate_tree)
