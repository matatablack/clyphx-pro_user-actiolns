from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from template.TemplateBase import TemplateBase

class Template(UserActionsBase):

    tpl = TemplateBase()

    def __init__(self, cx_core, *a, **k):
        super(Template, self).__init__(cx_core, *a, **k)
        self.tpl._do_init(self)

    def create_actions(self):
        self.add_global_action('tpl', self.entry_point_handler)

    def entry_point_handler(self, _, args):
        self.tpl.dispatch(args)

    def on_selected_track_changed(self):
        self.tpl.set_selected_track(self.song().view.selected_track)
