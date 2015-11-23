'''
Created on Nov 21, 2015

@author: george
'''
commands = {}
def command(cmd_name):
    def wrapper(cls):
        print "Registering command: {} with class: {}".format(cmd_name, cls)
        global commands
        commands[cmd_name] = cls
        return cls
    return wrapper

def create_command(*args, **kwargs):
    cmd = commands[args[0]]
    return cmd(*args[1:], **kwargs)

if __name__ == '__main__':
    pass