import subprocess
import shutil

def execute(cmd, capture=False):
    """Execute a command.
    
    :arg bool capture: If True then enter the capture mode: process output
        will be captured and the function will return a generator yielding
        lines of the output.
    :rtype: Iterator[str] or None
    """
    def do_execute():
        stdout = subprocess.PIPE if capture else None
        shell = True if isinstance(cmd, str) else False
        if not shell:
            executable = shutil.which(cmd[0])
            if executable:
                cmd[0] = executable
        with subprocess.Popen(cmd, stdout=stdout, encoding="utf8", shell=shell) as process:
            if capture:
                for line in process.stdout:
                    yield line
        if process.returncode:
            raise subprocess.CalledProcessError(process.returncode, cmd)
    if capture:
        return do_execute()
    list(do_execute())
    