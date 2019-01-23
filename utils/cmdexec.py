import os
import signal
import shlex
import subprocess
import threading
import time
import logging

# Global defines
SIGNALS=dict((k, v) for v, k in signal.__dict__.items() if v.startswith('SIG'))

class CmdExec():
  """
  Execute a command in a shell and communicate.
  """

    def __init__(self):
        super(CmdExec, self).__init__()
        self._process           = None
        self._processException  = None
        self._stdout            = None
        self._stderr            = None

    # execute a command
    def run(self,command,args=None,timeout=None,cwd=None):

        # Print command line
        # split arguments and prefix them with the command
        cmdLine = "{} {}".format(command,args)
        splitCmd = shlex.split(cmdLine)
        logging.info("Exec: \"{}\" in \"{}/{}\"".format(
                                                str(splitCmd),
                                                os.getcwd(),
                                                cwd if cwd is not None else ""
                                            ))

        # threaded execution
        def threadExec():
            # execute command
            try:
                self._process = subprocess.Popen(
                                                    splitCmd,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    cwd=cwd
                                                )
            except Exception as e:
                self._processException = e
            else:
                # fetch output 
                self._stdout, self._stderr = self._process.communicate()

        # do exec the cmd in a thread
        # we do this in order to stay python2.7 compatible
        thread = threading.Thread(target=threadExec)
        startTime = time.time()
        thread.start()

        # wait for execution to finish 
        thread.join(timeout)

        # check for exception
        if self._processException is not None:
            raise self._processException

        if thread.isAlive():
            logging.info("Execution timeout")
            self._process.kill()
            thread.join()
            return None, None, None, None, None
        endTime = time.time()

        # calculate run time
        runTime = endTime-startTime

        # fetch terminating signal
        # see: http://docs.python.org/3.3/library/subprocess.html?highlight=popen#subprocess.Popen
        if self._process.returncode < 0:
            signal=-self._process.returncode
        else:
            signal=None

        # convert output to string
        stdout=str(self._stdout,'utf-8')
        stderr=str(self._stderr,'utf-8')

        # is output a string?
        if not self._isString(stdout) \
           or not self._isString(stderr):
            logging.info("STDOUT or STDERR not a String!")
            return;

        #split lines up
        stdout = stdout.splitlines()
        stderr = stderr.splitlines()
        
        #then strip the strings in the list
        stdout = self._stripList(stdout)
        stderr = self._stripList(stderr)

        # filter out empty lines
        stdout = list(filter(None,stdout))
        stderr = list(filter(None,stderr))

        # print the data gathered during run
        logging.info("Command results:")
        logging.info("== RUNTIME ==")
        logging.info("{} seconds".format(runTime))
        logging.info("== RETURNCODE ==")
        logging.info("{}".format(self._process.returncode))
        logging.info("== SIGNAL ==")
        if signal is not None:
            if signal in SIGNALS:
                logging.info("{} : {}".format(signal,SIGNALS[signal]))
            else:
                logging.info("{} : unknown".format(signal))
        logging.info("== STDOUT ==")
        logging.infoList(stdout)
        logging.info("== STDERR ==")
        logging.infoList(stderr)

        return self._process.returncode, signal, stdout, stderr, runTime
