import copy

class Parser(object):
    def append_status(self, result):
        """parse the puppet kick result, and append a True/False Boolean Value to
        Result list of Result_Q
        Args:
            result: list, [host, stdout, stderr]
        Return:
            return a list: [host, stdout, stderr, status]
        """
        stderr = result[2]
        cp_result = copy.deepcopy(result)
        
        if stderr:
            # error handler step
            cp_result.append(False)
        else:
            # succ handler step
            cp_result.append(True)
        
        return cp_result