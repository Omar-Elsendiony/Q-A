import os
import shutil
import ast
import subprocess
from subprocess import PIPE


def getFaultyLines(folder_path):
    import csv
    # folder_path = 'O:/DriveFiles/GP_Projects/Bug-Repair/Q-A/'

    # filename = 'O:\DriveFiles\GP_Projects\Bug-Repair\FauxPyReport_Q-A_sbfl_statement_2024_04_28_22_54_49_084332\Scores_Tarantula.csv'
    # Get a list of all folders in the directory
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Find the folder that starts with 'FauxPy'
    fauxpy_folder = next((f for f in folders if f.startswith('FauxPy')), None)
    lines = []
    scores = []

    with open(f'../{fauxpy_folder}/Scores_Tarantula.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 2:
                # get only the line number 
                lineno = row[0].split('::')[1]
                lines.append(lineno)
                scores.append(row[1])

    # print(lines)
    # print(scores)
    return lines, scores


def deleteFolder(folder_path):
    # Get a list of all folders in the directory
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Find the folder that starts with 'FauxPy'
    fauxpy_folder = next((f for f in folders if f.startswith('FauxPy')), None)

    # Delete the folder if it exists
    if fauxpy_folder:
        shutil.rmtree(os.path.join(folder_path, fauxpy_folder))
        print(f"The folder '{fauxpy_folder}' has been deleted.")
    else:
        print("No folder starting with 'FauxPy' found.")


def copyFolder(source_folder, destination_folder, file_id):
    # file_id = 1
    # source_folder = f'O:\DriveFiles\GP_Projects\Bug-Repair\Q-A\MyMutpy/testcases\BuggyPrograms'
    # destination_folder = f'{directory_path}'
    file_name = f'{file_id}.txt'

    # Construct the source and destination file paths
    source_file_path = f'{source_folder}/{file_name}'
    destination_file_path = f'{destination_folder}/source_code.py'

    # Copy the file from the source folder to the destination folder
    shutil.copy(source_file_path, destination_file_path)

    print(f"File '{file_name}' copied from '{source_folder}' to '{destination_folder}'.")


def create_py_test(inputs, outputs, function_name, destination_folder):
    pytest_file = ""

    module_ast = ast.parse(pytest_file)
    import_str = "from source_code import *"
    import_node = ast.parse(import_str).body[0]

    # Add the import statement to the beginning of the AST
    module_ast.body.insert(0, import_node)

    # inputs = [[1, 2], [3, 4], [5, 6]]
    # outputs = [3, 7, 11]
    # function_name = "add"
    # function ast
    for i in range(len(inputs)):
        fn = f"""def test_{i}(): pass"""
        fn_ast = ast.parse(fn).body[0]
        input_str = f"inputs = "
        assert_str = f"assert "
        input_curr = inputs[i]

        if isinstance(input_curr, str):
            input_str += '"' + input_curr + '"'
            if (input_curr.lower() == "void"):
                assert_str += f"{function_name}() == {outputs[i]}"
        else:
            for input in input_curr:
                if (input == inputs[-1]):
                    input_str += f"{input}"
                else:
                    input_str += f"{input},"
            # input_node = ast.parse(input_str).body[0]
            assert_str += f"{function_name}(*inputs) == {outputs[i]}"
        
        input_node = ast.parse(input_str).body[0]
        assert_node = ast.parse(assert_str).body[0]
        # fn_ast.body.pop()

        fn_ast.body.append(input_node)
        fn_ast.body.append(assert_node)
        # print(ast.unparse(module_ast))

        module_ast.body.append(fn_ast)
        # Check if the destination folder exists
        if not os.path.exists(destination_folder):
            # Create the destination folder if it doesn't exist
            os.makedirs(destination_folder)
            print(f"The folder '{destination_folder}' has been created.")

        # Create the file within the destination folder
        file_path = os.path.join(destination_folder, "test.py")
        with open(file_path, "w") as file:
            # Convert the string to Python code
            python_code = ast.unparse(module_ast)
            file.write(python_code)

        print(f"File 'test.py' created in '{destination_folder}' with the converted Python code.")
        
    # print(ast.unparse(module_ast))
    # print(ast.dump(module_ast, indent=4))

def runFaultLocalization(test_path, src_path):
    # test_path = "O:\DriveFiles\GP_Projects\Bug-Repair\Q-A\MyMutpy\FaultLocalization/test/test_1.py"
    # src_path = "O:\DriveFiles\GP_Projects\Bug-Repair\Q-A\MyMutpy\FaultLocalization/test/src.py"
    # python -m pytest .\MyMutpy\FaultLocalization\test\test_1.py   --src .\MyMutpy\FaultLocalization\test\src.py  --family sbfl  --granularity statement --top-n 14
    return subprocess.run(["python3", "-m", "pytest", f"{test_path}", "--src", f"{src_path}", "--family", "sbfl", "--granularity", "statement", "--top-n" , "25"], stderr=subprocess.PIPE)


def main(inputs, outputs, function_name, source_folder, destination_folder, file_id):
    # delete the folder of the fault localization if found
    folder_path = '..'
    deleteFolder(folder_path)

    # Copy the file from the source folder to the destination folder
    copyFolder(source_folder, destination_folder, file_id)

    # Create the PyTest file with the test cases
    create_py_test(inputs, outputs, function_name, destination_folder)

    # Run the fault localization tool
    test_path = f'{destination_folder}/test.py'
    src_path = f'{destination_folder}/source_code.py'
    runFaultLocalization(test_path, src_path)

