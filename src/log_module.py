''' Log module '''


class log_module:
    '''
    Class log_module initializes logs
    '''
    def __init__(self):
        '''
        Function Name: __init__
        Purpose: Initialize a log_module Class
        Parameters: self
        Return Value: None
        Algorithm: Initialize logs with default value
        '''
        self.logs = []

    def new_log(self, message):
       '''
        Function Name: new_log
        Purpose: Append a log to the list of logs
        Parameters: self, message
        Return Value: None
        Algorithm: Append a log to the list of logs
        '''
       self.logs.append(message)

    def fetch_log(self):
        '''
        Function Name: fetch_log
        Purpose: Fetch all the logs for the game
        Parameters: self
        Return Value: logs
        Algorithm: Return the logs list
        '''
        return self.logs
