# Minimal example of my class-based ClyphX script registration (able to preserve state across calls


def register(trg):
    trg._parent.log_message('Registering UserAction command from:%s' % __file__)

    # create object and store on ClyphXUserAction class
    obj = MyClyphXCmd()  # object isn't GC'ed I think because the closure maintains a reference to it

    # maps name of ClyphX command to method on ClyphXUserAction class
    trg._action_dict['GNIP_MINIMAL_OBJ'] = 'gnip_minimal_obj_router_method'

    # create closure to to route method call from ClyphXUserAction class to this custom class AND hold a reference to "obj"
    def method_router(trg, track, args):
        """Called by the method on ClyphXUserAction and delegates the call to a method on our custom object"""
        obj.do_cmd(trg, track, args)

    # add router method to ClyphXUserAction class
    type(trg).gnip_minimal_obj_router_method = method_router  # add method to ClyphXUserAction class


class MyClyphXCmd:
    def __init__(self):
        self.val = 42

    def do_cmd(self, trg, track, args):
        self.val += 1
        for track in trg.song().tracks:
            trg._parent.log_message('Track %s' % track.name)
        trg._parent.show_message('Value:%d Args:%s ' % (self.val, args))