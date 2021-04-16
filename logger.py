"""
Created on Wed Apr 14 2021 22:35:33 

@author: PS Chauhan
"""

"""
This module implements the logger in order keep the log of some events
which can be further used for debugging purposes    
"""

import logging

class Log:

    def __init__(self):

        #config
        logging.basicConfig(filename="log_file.log", format='%(asctime)s %(process)d %(levelname)s %(message)s', filemode='w')

        #creating object
        self.logger = logging.getLogger()
    
    def addLog(self,level,msg):
        #only msg with warning and above are allowed
        if level == 'warning' :
            self.logger.warning(msg)
        elif level == 'error':
            self.logger.error(msg)
        elif level == 'critical':
            self.logger.critical(msg)
        else:
            self.logger.critical('invalid level is used ')
        




