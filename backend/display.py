import json
import time

debate_tree = json.load(
    open("/home/mcosson/code/hackaton/SCH/backend/debate_tree.json", "r")
)


def generate_paths_to_leaf(tree, node_id, current_path, paths):
    if "question" in tree[node_id]:
        current_path.append(node_id)
        for next_node_key in tree[node_id]["answers"].values():
            generate_paths_to_leaf(tree, next_node_key, current_path, paths)
        current_path.pop()
    elif "action" in tree[node_id]:
        current_path.append(node_id)
        paths.append(current_path.copy())
        current_path.pop()


paths = []
generate_paths_to_leaf(debate_tree, "0", [], paths)
for path in paths:
    print(path)


def find_path(paths, leaf_id):
    for p in paths:
        if p[-1] == leaf_id:
            return p
    return []


def display_path(tree, paths, leaf_id):
    path = find_path(paths=paths, leaf_id=leaf_id)
    for i, node_id in enumerate(path):
        node = tree[node_id]
        if "question" in node:
            print("[TREE QUESTION]", node["question"])
            time.sleep(0.5)
            for answer, next_node_id in node["answers"].items():
                if next_node_id == path[i + 1]:
                    print("[MODEL]", "YES" if answer == "yes" else "NO")
                    time.sleep(0.5)
        elif "action" in node:
            print("[OUTPUT PROMPT]", node["action"])
            time.sleep(0.5)


for leaf in ["5a2b2b", "4a", "8b"]:
    display_path(tree=debate_tree, paths=paths, leaf_id=leaf)
