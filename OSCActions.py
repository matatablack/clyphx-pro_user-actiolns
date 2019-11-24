from ClyphX_Pro.clyphx_pro.ParseUtils import parse_number
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase


class OSCActions(UserActionsBase):
    """ OSCActions handles sending out OSC messages. """

    def __init__(self, cx_core, *a, **k):
        super(OSCActions, self).__init__(cx_core, *a, **k)
        self._server = None
        self.canonical_parent.schedule_message(2, self._do_init, cx_core)

    def disconnect(self):
        super(OSCActions, self).disconnect()
        self._server = None

    def create_actions(self):
        self.add_global_action('osc', self._send_osc_message)

    def _do_init(self, cx_core):
        # need to use scheduling here as user actions are created before the OSC server.
        self._server = cx_core.osc_server

    def _send_osc_message(self, _, args):
        if self._server and args:
            args = args.split()
            if len(args) > 2:
                msg_type = args[0]
                address = args[1]
                msg = ' '.join(args[2:])
                if msg_type == 'str':
                    # not entirely sure why we need to do this with address
                    # but it's unreliable without it
                    self._server.sendOSC(str(address), str(msg[1:-1]))
                elif msg_type == 'flt':
                    self._server.sendOSC(address, parse_number(msg, default_value=0.0,
                                                               is_float=True))
                else:
                    self._server.sendOSC(address, parse_number(msg, default_value=0))
