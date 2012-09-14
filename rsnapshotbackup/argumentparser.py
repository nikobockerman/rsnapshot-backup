'''
http://stackoverflow.com/a/5943381
'''

import argparse
import sys

class ArgParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        """Initialisation method for the parser class"""
        super(ArgParser,  self).__init__(*args,  **kwargs)
        #argparse.ArgumentParser.__init__(self, *args, **kwargs)
    
    def _get_action_from_name(self, name):
        """Given a name, get the Action instance registered with this parser.
        If only it were made available in the ArgumentError object. It is 
        passed as it's first arg...
        """
        container = self._actions
        if name is None:
            return None
        for action in container:
            if '/'.join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action
    
    def error(self, message):
        exc = sys.exc_info()[1]
        if exc:
            exc.argument = self._get_action_from_name(exc.argument_name)
            raise exc
        raise argparse.ArgumentError(None,  message)

if __name__ == "__main__":
    print ("Starting")
    parser = ArgParser()
    parser.add_argument('foo')
    parser.add_argument('boo')
    try:
        parser.parse_args(['fsdf'])
        print ("Successfully parsed arguments")
    except argparse.ArgumentError as exc:
        print ("Exception caught:")
        print (exc.message)
        if exc.argument is not None:
            print (exc.argument)
        
