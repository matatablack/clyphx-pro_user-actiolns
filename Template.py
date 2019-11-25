from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

""" The number of X-Controls to add shift functionality to. """
NUM_X_CONTROLS = 100


class Template(UserActionsBase):
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

        # def on_selected_track_changed(self):
    #     # trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
    #     track = self.song().selected_track
    #     self.canonical_parent.show_message('new track name: %s' % track.name)
        def record_midi_to_audio(self, action_def, args):
        track = action_def['track']
        track.arm.value = True
        self.canonical_parent.show_message('track name is')

        MSG \"HOLA %s\"

    """

    def create_actions(self):
        """ Create the action.  We define it as a global action since it's not specific
        to a track, device or clip. """
        self.add_global_action('tpl', self.handler)

    def handler(self, _, args):
        trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        trigger("SEL/MUTE;")
        count = 1
        self.canonical_parent.log_message('Count: %s' % count)
        self.canonical_parent.show_message('Count: %s' % count)