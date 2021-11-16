from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

""" The number of X-Controls to add shift functionality to. """
NUM_X_CONTROLS = 100


class ShiftAction(UserActionsBase):
    """
    ShiftAction creates an action named shift that shifts macro assignments between
    a default and shifted layer for use in creating shift functionality for X-Controls.
    
    The X-Control to use as a shift button should look something like this:
    shift_button = note, 1, 98, 0, 127, shift on : shift off

    So, shift_button will trigger shift on when pressed and shift off when released.
    
    Each X-Control to add shift functionality to should look something like this:
    b1 = note, 1, 0, 0, 127, $b1$
    
    So, b1 will trigger the macro named $b1$.
    
    Macros should be of the following form for each X-Control:
    $b1_default$ = mute
    $b1_shifted$ = solo
    $b1$ = $b1_default$
    
    So, $b1$ will be assigned to $b1_default$ by default and $b1_shifted$ when
    shift_button is held down.
    """

    def create_actions(self):
        """ Create the action.  We define it as a global action since it's not specific
        to a track, device or clip. """
        self.add_global_action('shift', self._handle_shift)

    def _handle_shift(self, _, args):
        trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        log = self.canonical_parent.clyphx_pro_component.log_message

        splitedArgs = args.split()
        prefix = splitedArgs[0]
        state = splitedArgs[1]
        
        footer = 'shifted' if state and state == 'on' else 'default'
        for i in xrange(1, NUM_X_CONTROLS):
            res = '${prefix}{index}$=${prefix}{index}_{footer}$'.format(prefix=prefix, index=i, footer=footer)
            trigger(res)
