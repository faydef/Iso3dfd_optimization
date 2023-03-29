from subprocess import STDOUT, check_output
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
        output = result.group(1)
        output = float(output.strip())

    #    except subprocess.TimeoutExpired:
    except Exception as e:
        print("#####algo stopped running: ", e)
        output = -99
    return output


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
    command = command + " | grep " + output_value
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
        print(output)
        output = output.decode("UTF-8")
        result = re.search("all energy: (.*)", output)
        print(result)
        output = result.group(1)
        print(output)
        output = float(output.strip())

    #    except subprocess.TimeoutExpired:
    except Exception as e:
        print("#####algo stopped running: ", e)
        output = 1000
    return output


# execute('cat test.txt | grep flops', 10)
