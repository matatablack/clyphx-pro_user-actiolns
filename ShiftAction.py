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
        """ This is the code that handles shifting the macro assignments.  Super simple,
        but let's go through it line by line. """

        # fnc is the function we use for triggering action lists.
        fnc = self.canonical_parent.clyphx_pro_component.trigger_action_list

        # footer is the last part of the macro name we want to use - shifted when
        # shift on is called and default when shift off is called.
        footer = 'shifted' if args and args == 'on' else 'default'

        # trigger NUM_X_CONTROLS action lists
        for i in xrange(1, NUM_X_CONTROLS):

            # generate the action list, which is just a macro assignment in this case
            # the result that will be passed to fnc will look something like this:
            # $b1$=$b1_shifted$ or $b1$=$b1_default$
            fnc('$b%s$=$b%s_%s$' % (i, i, footer))
