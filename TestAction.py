from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase

class TestAction(UserActionsBase):

    def create_actions(self):
        self.add_global_action('test_action', self.global_action_handler)
        self.add_track_action('test_track', self.track_action_handler)


    def record_midi_to_audio(self, action_def, args):
        track = action_def['track']
        track.arm.value = True
        self.canonical_parent.show_message('track name is')


    def global_action_handler(self, action_def, args):
        trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        self.canonical_parent.show_message('%s: Hello World' % args)
        trigger('MSG global action triggered')
        
        # for i in device.parameters
        #     trigger( #how to write this )

        #return_chain_fx_device = getattr(myobject, 'some_value', None)

    # def test_dev_handler(self, actions_def, args):
    #     dev = actions_def['device']
    #     self.trigger('MSG device name is %s', dev.name)

    # def test_clip_handler(self, actions_def, args):
    #     clip = actions_def['clip']
    #     self.trigger('MSG clip names is %s', clip.name)
        



"""
snippets & ideas

track.arm.set
track.color.set
track.fired_slot_index
track.available_input_routing_channels
track.available_input_routing_types.get
track.input_routing_channel.get





"""