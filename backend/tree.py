debate_tree = {
    "0": {
        "question": "Is the opponent's argumentation already developed?",
        "answers": {"yes": "1", "no": "7"},
    },
    "1": {
        "question": "Does their argumentation put us at a disadvantage?",
        "answers": {"yes": "2", "no": "5"},
    },
    "2": {
        "question": "Is the opponent attacking our thesis directly?",
        "answers": {"yes": "3", "no": "4"},
    },
    "3": {"question": "Is the attack objective?", "answers": {"yes": "3a", "no": "3b"}},
    "3a": {
        "action": "Assume what needs to be proved, either under another name, by asserting a contested particular truth as a general truth, or by deriving all particular truths from a general truth.",
        "id": "1111",
    },
    "3b": {
        "action": "Check if some of the opponent's statements are not in contradiction with others, depending on the perspective from which they are considered.",
        "id": "1110",
    },
    "4": {
        "question": "Can we use the opponent's statements against them?",
        "answers": {"yes": "4a", "no": "4b"},
    },
    "4a": {
        "action": "Check if some of the opponent's statements are not in contradiction with others, depending on the perspective from which they are considered.",
        "id": "1101",
    },
    "4b": {
        "action": "Show impudence. Anger the opponent, because in their fury, they are unable to judge correctly or see their own interest.",
        "id": "1100",
    },
    "5": {
        "question": "Are the foundations of the opponent's thesis solid?",
        "answers": {"yes": "5a", "no": "6"},
    },
    "5a": {
        "question": "Can the thesis consequences be used against it?",
        "answers": {"yes": "5a1", "no": "5a2"},
    },
    "5a1": {
        "question": "Does associating the thesis with a recognized truth lead to a contradiction?",
        "answers": {"yes": "5a1a", "no": "5a1b"},
    },
    "5a1a": {
        "action": "Apagogue - The art of deriving false conclusions: force the opponent's thesis to yield contradictory or general truths contradicting propositions not found in the thesis itself, thereby constructing an indirect refutation, an apagogue or reasoning by absurdity.",
        "id": "10111",
    },
    "5a1b": {"action": "Find a contradictory example", "id": "10110"},
    "5a2": {
        "question": "Is the opponent in a position of strength?",
        "answers": {"yes": "5a2a", "no": "5a2b"},
    },
    "5a2a": {"action": "Diversion", "id": "10101"},
    "6": {
        "action": "Last-Resort Diversion - Use diversion as a last resort if defeat seems imminent. Talk about something entirely different as if it were part of the debated subject, with varying degrees of discretion or impudence.",
        "id": "100",
    },
    "5a2b": {
        "question": "Can we demonstrate that the foundations are false?",
        "answers": {"yes": "5a2b1", "no": "5a2b2"},
    },
    "5a2b1": {
        "action": "Assume what needs to be proved, either under another name, by asserting a contested particular truth as a general truth, or by deriving all particular truths from a general truth.",
        "id": "101001",
    },
    "5a2b2": {
        "question": "Honest or not?",
        "answers": {"yes": "5a2b2a", "no": "5a2b2b"},
    },
    "5a2b2a": {
        "action": "Strengthen the attack - Assume what needs to be proved, either under another name, by asserting a contested particular truth as a general truth, or by deriving all particular truths from a general truth.",
        "id": "1010001",
    },
    "5a2b2b": {
        "action": "Mischievous Trick - Fallacy of non causa pro causa - present a reason as though it were a cause: when the opponent has answered several questions unfavorably, yet declare that the deduction we wanted to achieve is proven.",
        "id": "1010000",
    },
    "7": {
        "question": "Is the opponent's thesis clearly defined?",
        "answers": {"yes": "8", "no": "9"},
    },
    "8": {
        "question": "Does the thesis contradict previous statements of the opponent (ad hominem)?",
        "answers": {"yes": "8a", "no": "8b"},
    },
    "8a": {"action": "Ad hominem argument to highlight contradictions", "id": "011"},
    "8b": {
        "action": "The art of deriving false conclusions: force the opponent's thesis to yield contradictory or general truths contradicting propositions not found in the thesis itself, thereby constructing an indirect refutation, an apagogue or reasoning by absurdity.",
        "id": "010",
    },
    "9": {
        "action": "Stretch the opponent's claim beyond its natural limits, interpret it as broadly as possible, take it in the widest sense, and exaggerate. At the same time, reduce your own claim to the strictest possible sense: the more general a claim becomes, the more vulnerable it is to attack.",
        "id": "00",
    },
}


import json
import concurrent.futures
import random
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from dotenv import load_dotenv

load_dotenv(".env")

MISTRAL_API_TOKEN = os.getenv("MISTRAL_API_TOKEN")

model = "mistral-large-latest"
client = MistralClient(api_key=MISTRAL_API_TOKEN)

a_prompt_template = """You are in a debate.

Here is the history of the debate you are in:
{history}

You are replying to your opponent. Use the strategy below:
{action}

Don't always be polite. You can be snarky.
"""


q_prompt_template = """You are in a debate.

Here is the history of the debate you are in:
{history}

You are analysing the opponent's arguments. Based on your analysis, answer the question below:
{question}

Only reply \"yes\" or \"no\". Do not answer anything else, do not describe your thoughts. Merely just answer \"yes\" or \"no\"."""


# Function to get response from AI
def get_ai_response(prompt):
    response = client.chat(
        model=model, messages=[ChatMessage(role="user", content=prompt)]
    )
    return response.choices[0].message.content


def q_response_parse(string):
    if "yes" in string.lower():
        return "yes"
    elif "no" in string.lower():
        return "no"
    return "err"


def process_debate(history_item):
    current_node = debate_tree["0"]
    while "question" in current_node:
        formatted_question = q_prompt_template.format(
            history=history_item, question=current_node["question"]
        )
        ai_answer = get_ai_response(formatted_question)
        next_node_id = current_node["answers"][q_response_parse(ai_answer)]
        current_node = debate_tree[next_node_id]
    if "action" in current_node:
        formatted_action = a_prompt_template.format(
            history=history_item, action=current_node["action"]
        )
        ai_action_response = get_ai_response(formatted_action)
        return {
            "history": history_item,
            "action_id": current_node["id"],
            "response": ai_action_response,
        }
    else:
        return {
            "history": history_item,
            "action_id": None,
            "response": "No action available",
        }


def main():
    with open("histories.json", "r") as f:
        histories_data = json.load(f)
    histories = list(histories_data.values())
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_debate, histories))
    with open("debate_results.json", "w") as f_out:
        json.dump(results, f_out)


if __name__ == "__main__":
    main()
