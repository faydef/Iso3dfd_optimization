from subprocess import STDOUT, check_output
import os
import re
from test_nrj import csv_to_energy



def execute(bash_command, timeout, output_value="flops"):
    try:
        output = check_output(bash_command, timeout=timeout, shell=True)
        output = output.decode("UTF-8")
        if output_value == "flops":
            result = re.search("flops:(.*) GFlops", output)
        elif output_value == "points":
           result = re.seatch("flops:(.*) MPoints/s", output)
        result = result.group(1)
        result = float(result.strip())
        time = re.search('time:(.*) sec', output)
        tmp = time.group(1)
        time = float(tmp.strip())


    #    except subprocess.TimeoutExpired:
    except Exception as e:
        print("#####algo stopped running: ", e)
        result = -99
        time = timeout

    return result,time


def command(options, output_value="flops"):
    command = (
        options["filename"]
        + " "
        + options["size1"]
        + " "
        + options["size2"]
        + " "
        + options["size3"]
        + " "
        + options["num_thread"]
        + " 100"
        + " "
        + options["dim1"]
        + " "
        + options["dim2"]
        + " "
        + options["dim3"]
    )
    #command = command + " | grep " + output_value
    return command


def command_nrj(options):
    command1 = (
        "/opt/cpu_monitor/cpu_monitor.x --csv --quiet --redirect -- "
        + options["filename"]
        + " "
        + options["size1"]
        + " "
        + options["size2"]
        + " "
        + options["size3"]
        + " "
        + options["num_thread"]
        + " 100"
        + " "
        + options["dim1"]
        + " "
        + options["dim2"]
        + " "
        + options["dim3"]
    )
    return command1


def execute_nrj(bash_command, timeout):
    try:
        output = check_output(bash_command, timeout=timeout, shell=True)
        parse_output = "python test_nrj.py -f $(ls -t1 ./*.csv | head -n1) | grep all"
        output = check_output(parse_output, timeout=timeout, shell=True)
        output = output.decode("UTF-8")
        result = re.search("all energy: (.*)", output)
        output = result.group(1)
        output = float(output.strip())

    #    except subprocess.TimeoutExpired:
    except Exception as e:
        print("#####No need to explore this path: ", e)
        output = 1000
    return 1/(output+1)


def mixed_exec(options, timeout, alpha, output_value="flops"):
    bash_perf = command(options)
    bash_nrj = command_nrj(options)
    perf = execute(bash_perf, timeout, output_value)
    nrj = execute_nrj(bash_nrj, timeout)
    return alpha * perf + (1 - alpha) * nrj

def execute_all(bash_command, timeout):
    try:
        _ = check_output(bash_command, timeout=timeout, shell=True)
        parse_output = "python test_nrj.py -f $(ls -t1 ./*.csv | head -n1) | grep all"
        output = check_output(parse_output, timeout=timeout, shell=True)
        output = output.decode("UTF-8")
        result = re.search("all energy: (.*)", output)
        output = result.group(1)
        output = float(output.strip())

    #    except subprocess.TimeoutExpired:
    except Exception as e:
        print("#####No need to explore this path: ", e)
        output = -99
    return output

def mixed(options, timeout, alpha, output_value="GFlops"):
    bash_perf = command(options, output_value)
    # Create a new file with the command
    with open("my_script.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write('../'+bash_perf+' > result.txt')

    # Make the file executable
    os.chmod("my_script.sh", 0o755)
    bash_command = 'cd results && /opt/cpu_monitor/cpu_monitor.x --csv --quiet --redirect -- ../my_script.sh && cd ..'
    try:
        _ = check_output(bash_command, timeout=timeout, shell=True)
        parse_output = "python test_nrj.py -f $(ls -t1 results/*.csv | head -n1) | grep all"
        output = check_output(parse_output, timeout=timeout, shell=True)
        output = output.decode("UTF-8")
        result = re.search("all energy: (.*)", output)
        output = result.group(1)
        output = float(output.strip())
        with open('results/result.txt', 'r') as f:
            for line in f:
                if 'GFlops' in line:
                    score =  line.rstrip('\n')
                    score = re.search(f"flops:(.*) {output_value}", score)
                    score = score.group(1)
                    score = float(score.strip())
                if 'time' in line:
                    time =  line.rstrip('\n')
                    time = re.search(f"time:(.*) sec", score)
                    time = score.group(1)
                    time = float(score.strip())
        output = alpha*(score/100) + (1-alpha)/(output*100)

    #    except subprocess.TimeoutExpired:
    except Exception as e:
        print("#####No need to explore this path: ", e)
        output = -99
    return output, time






# execute('cat test.txt | grep flops', 10)
