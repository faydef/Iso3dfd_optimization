from subprocess import STDOUT, check_output
import re
def execute(bash_command, timeout,output_value='flops'):
    try:
        output = check_output(bash_command, timeout=timeout, shell=True)
        output = output.decode('UTF-8')
        if output_value == 'flops' :
            result = re.search('flops:(.*) GFlops', output)
        elif output_value == 'points' :
            result = re.seatch('flops:(.*) MPoints/s', output)
        output = result.group(1)
        output = float(output.strip())

#    except subprocess.TimeoutExpired:
    except Exception as e:
        print("#####algo stopped running: ",e)
        output = 0
    return output

def command(options,output_value='flops'):
    command = options['filename']+' '+options['size1']+' '+options['size2']+' '+options['size3']+' '+options['num_thread']+' 100'+' '+options['dim1']+' '+options['dim2']+' '+options['dim3']
    command = command + ' | grep ' + output_value
    return command

#execute('cat test.txt | grep flops', 10)


