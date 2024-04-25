##################### CODE DIFFERENCE UTILITY #####################
import code_diff as cd

from code_diff.gumtree import ops

def _subtrees(script):
    subtrees = {}
    for action in script:
        if not isinstance(action, (ops.Insert, ops.Move)): continue
        target, node, position = action.target_node, action.node, action.position

        if isinstance(action, ops.Insert):
            _, text = node
            insert_content = text if text is not None else action.insert_id
            subtrees[(action.insert_id)] = (insert_content)
            # target_id = target.node_id
            # if target_id not in subtrees: subtrees[target_id] = []
            # else: subtrees[target_id] = []
            # subtrees[target_id].insert(position, insert_content)
        elif isinstance(action, ops.Move):
            insert_content = node
            # subtrees[str(action.move_id)] = (insert_content)

        # if hasattr(target, "node_id"):
        #     target_id = target.node_id
        #     if target_id not in subtrees: subtrees[target_id] = []
        #     else: subtrees[target_id] = []
        #     subtrees[target_id].insert(position, insert_content)
    
    return subtrees

def _serialize_tree(subtrees, node_id):
    result = []
    stack  = [node_id]

    while len(stack) > 0:
        element = stack.pop(0)
        if isinstance(element, int):
            # element = str(element)
            elem = subtrees.get(element, [])
            if (elem != []):
                result.append(elem)
            else:
                stack = subtrees.get(element, []) + stack
        else:
            result.append(element)

    return result

def flatten_script(script):
    result_script = []
    subtrees = _subtrees(script)

    for action in script:
        if isinstance(action, ops.Insert):
            if not hasattr(action.target_node, "node_id"): continue # Ignore because we flatten
            new_node = _serialize_tree(subtrees, action.insert_id)
            result_script.append(ops.Insert(action.target_node, new_node, position = action.position, insert_id=action.insert_id))
        elif isinstance(action, ops.Move) and hasattr(action.target_node, "node_id"):
            result_script.append(ops.Delete(action.node))
        else:
            result_script.append(action)

    return result_script

def synthesize_rewrite_script(script):
    # Flatten the script: Build and parse the subtrees that are inserted or moved
    flat_script = flatten_script(script)

    # Generate new actions of the form (replace_span, token_seq)
    # You can transform the source by replacing each span with the token sequence 
    result = []
    for action in flat_script:
        target_node = action.target_node
        if isinstance(action, ops.Insert):
            if action.position == len(target_node.children):
                (start_line, start_pos), (end_line, end_pos) = target_node.position[1], target_node.position[1]
            else:
                if (target_node.children == []): continue
                predecessor = target_node.children[action.position]
                (start_line, start_pos), (end_line, end_pos) = predecessor.position[1], predecessor.position[1]

            result.append(((start_line, start_pos, end_line, end_pos), action.node))
        elif isinstance(action, ops.Update):
            (start_line, start_pos), (end_line, end_pos) = target_node.position
            result.append(((start_line, start_pos, end_line, end_pos), [action.value]))
        elif isinstance(action, ops.Delete):
            (start_line, start_pos), (end_line, end_pos) = target_node.position
            deleteOperation = f'Delete: {(target_node).type}'
            result.append(((start_line, start_pos, end_line, end_pos), [deleteOperation]))

    return result

###################################################################################

output = cd.difference(
    '''
        expected = datetime . datetime ( 1970 , 1 , 1 , 1 , 0 , 23 , 0 , datefmt . localtz )
    ''',
    '''
        expected = datetime . datetime . fromtimestamp ( 23 , datefmt . localtz )
    ''',
lang = "python")



s = output.edit_script()
# s = synthesize_rewrite_script(s)
# print((s))

# Open the file in write mode
# with open('O:\DriveFiles\GP_Projects\Bug-Repair\Q-A\MyMutpy\output.txt', 'w') as file:
#     for action in s:
#         (start_line, start_pos, end_line, end_pos), new_content = action
#         file.write(f"{start_line} {start_pos} {end_line} {end_pos} {new_content}\n")

import json

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        line_content = [json.loads(line) for line in f.readlines()]
    return line_content
data = read_json_file('O:\DriveFiles\GP_Projects\ctssb_data_1M\ctssb_data_1M/file-0.jsonl/file-0.jsonl')
import ast

print(data[31]["before"])
print(data[31]["after"])
# print(data[1]["comodified"])
print(data[31]["edit_script"])
# print(data[631]["likely_bug"])

# s = ast.dump(ast.parse(data[31]["before"]), indent=4)
print("-------------------------------------")
diff = cd.difference(data[31]["before"], data[31]["after"], lang="python")
actions = synthesize_rewrite_script(diff.edit_script())
for action in actions:
    print(action)
