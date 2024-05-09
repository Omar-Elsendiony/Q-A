from glob import glob
from subprocess import Popen, PIPE, STDOUT
import subprocess
from subprocess import TimeoutExpired
import win32api
import win32process
import os
import shutil
MAX_VIRTUAL_MEMORY = 4 * 1024 * 1024 * 1024  # 4*1024 MB

import threading
import psutil


def only_digits(num):
    return num.replace("-", "").replace("+", "").replace('.','',1).replace("E","").isdigit()

def check_floating(n1, n2):
    if (not only_digits(n1)) or (not only_digits(n2)):
        return False
    #print(float(n1), float(n2))
    if abs(float(n1)-float(n2))<1e-6:
        return True
    return False


def compare_files(file1, file2):
    try:
        with open(file1) as f1, open(file2) as f2: 
            content1 = f1.read().strip().split()
            content2 = f2.read().strip().split()
            #print(content1)
            #print("########")
            #print(content2)
            if(len(content1) != len(content2)):
                #print("length not same")
                #print(content1)
                #print("#####")
                #print(content2)
                return False
            for l1, l2 in zip(content1, content2):
                if l1.strip() != l2.strip(): 
                    num1s = l1.strip().split(" ")
                    num2s = l2.strip().split(" ")
                    if(len(num1s) == len(num2s)):
                        for idx in range(len(num1s)):
                            if not check_floating(num1s[idx],num2s[idx]):
                                #print_error(l1, l2)
                                return False
                    else:
                        #print_error(l1, l2)
                        return False
            
            return True
    except Exception as e:
        print("exception = ", e)
        return False

def kill(proc_pid):
    if psutil.pid_exists(proc_pid):
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            if psutil.pid_exists(proc.pid):
                proc.kill()
        process.kill()


def run_python(code, test_case_folder, idx):
    root_path = f'garbage_py/{idx}'
    isExist = os.path.exists(root_path)
    if not isExist:
        os.makedirs(root_path)

    with open(f'{root_path}/Main.py', 'w+', encoding='utf8') as fw:
        fw.write(code)
    in_files = glob(test_case_folder+"/in/*")
    p1 = subprocess.run(["python","-m", "py_compile", f"{root_path}/Main.py"], stderr=PIPE)
    return_code = p1.returncode
    python2 = False
    if (return_code):
        p1 = subprocess.run(["python2","-m", "py_compile", f"{root_path}/Main.py"], stderr=PIPE)
        return_code = p1.returncode
        python2=True

    if(return_code):
        print("doesnt compile", return_code)
        return False, 0, len(in_files)

    did_not_match = 0
    for in_file in in_files:
        stripped_TC = open(in_file).read().strip()
        with open(f'{root_path}/stripped_TC.txt', 'w+') as f:
            f.write(stripped_TC)
        cmd = f"python {root_path}/Main.py < {root_path}/stripped_TC.txt > {root_path}/cmd_out.txt"
        if (python2):
            cmd = cmd.replace("python", "python2")
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.DEVNULL, close_fds=True)

        # for Time limit exceeded cases
        try:
            outs, errs = p.communicate(timeout=15)
        except TimeoutExpired:
            kill(p.pid)
            did_not_match+=1
            continue
        
        out_file = in_file.replace("in", "out", 1).replace(".in", ".out", 1)
        # print(f"{root_path}/cmd_out_match.txt")
        # print(out_file)
        shutil.copy(out_file, f"{root_path}/cmd_out_match.txt")
        # p2.wait()
        if not compare_files(f'{root_path}/cmd_out.txt', f'{root_path}/cmd_out_match.txt'):
            did_not_match+=1
            #print(in_file)
    
    shutil.rmtree(root_path)
    return True, len(in_files)-did_not_match,len(in_files)
