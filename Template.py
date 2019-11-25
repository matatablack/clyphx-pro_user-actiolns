from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from template.TemplateBase import TemplateBase

""" The number of X-Controls to add shift functionality to. """
NUM_X_CONTROLS = 100


class Template(UserActionsBase):
    """
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

    def __init__(self, cx_core, *a, **k):
        super(Template, self).__init__(cx_core, *a, **k)
        self.val = 42

    def create_actions(self):
        """ Create the action.  We define it as a global action since it's not specific
        to a track, device or clip. """
        self.add_global_action('tpl', self.handler)
        self.add_global_action('check', self.check)

    def handler(self, _, args):
        trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        trigger("wait 10; MSG \"yay user action\";")
        count = 1
        tpl = TemplateBase(trigger)
        tpl.handler(self.val)
        # tpl.handler(self, trigger)
        self.canonical_parent.log_message('Count: %s' % count)
        # self.canonical_parent.show_message('Count: %s' % count)
    def check(self, _, args):
        # trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        # trigger('MSG "yay user action"')
        self.canonical_parent.show_message('CHECK')