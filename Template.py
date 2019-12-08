from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from template.TemplateBase import TemplateBase

class Template(UserActionsBase):

    tpl = TemplateBase()

    def __init__(self, cx_core, *a, **k):
        super(Template, self).__init__(cx_core, *a, **k)
        self.tpl._do_init(self)

    def create_actions(self):
        self.add_global_action('tpl', self.entry_point_handler)
        self.add_clip_action('get_clip', self.get_clip)
        self.add_track_action('get_track', self.get_track)

    def entry_point_handler(self, _, args):
        trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        self.tpl.dispatch(args, trigger)

    def get_clip(self, action_def, args):
        clip = action_def['clip']
        self.tpl.set_target_clip(clip)

    def get_track(self, action_def, args):
        track = action_def['track']
        self.tpl.set_target_track(track)

    def on_selected_track_changed(self):
        self.tpl.set_selected_track(self.song().view.selected_track)
