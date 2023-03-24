from subprocess import STDOUT, check_output
import re
def execute(bash_command, timeout):
    try:
        output = check_output(bash_command, timeout=timeout, shell=True)
        output = output.decode('UTF-8')
        output2 = output
        result = re.search('flops:(.*) GFlops', output)
        time = re.search('time:(.*) sec', output2)
        tmp = time.group(1)
        time = float(tmp.strip())
        output = result.group(1)
        output = float(output.strip())

#    except subprocess.TimeoutExpired:
    except Exception as e:
        print("#####algo stopped running: ",e)
        output = -99
        time = timeout
    return output, time

def command(options):
    command = options['filename']+' '+options['size1']+' '+options['size2']+' '+options['size3']+' '+options['num_thread']+' 100'+' '+options['dim1']+' '+options['dim2']+' '+options['dim3']
    command = command + ' | grep flops'
    return command

#execute('cat test.txt | grep flops', 10)


