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


def recursive_process(node, indent=""):
    if "answers" in node.keys():
        for key in node["answers"].keys():
            node_key = node["answers"][key]
            ans_node = debate_tree[node_key]
            if key == "yes":
                print(indent + node["question"])
            recursive_process(ans_node, " " * 10)
    else:
        print(indent + node["id"])


for key in debate_tree.keys():
    recursive_process(debate_tree[key])