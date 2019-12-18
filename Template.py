from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from ClyphX_Pro.clyphx_pro.consts import DATA_HEADER
from template.TemplateBase import TemplateBase

class Template(UserActionsBase):

    tpl = TemplateBase()

    def __init__(self, cx_core, *a, **k):
        super(Template, self).__init__(cx_core, *a, **k)
        self.tpl._do_init(self)

    def create_actions(self):
        self.add_global_action('tpl', self.dispatch)
        self.add_clip_action('get_clip', self.get_clip)
        self.add_track_action('get_track', self.get_track)
        self.add_global_action('recallsnap', self.recallsnap)

    def dispatch(self, _, args):
        trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        self.tpl.dispatch(args, trigger)

    def get_clip(self, action_def, args):
        clip = action_def['clip']
        self.tpl.set_target_clip(clip)

    def get_track(self, action_def, args):
        track = action_def['track']
        self.tpl.set_target_track(track)
    
    def recallsnap(self, action_def, args):
        try:
            ident = args
            self.tpl.log('called recall snap with %s' % ident)
            if ident is not None:
                comp = self.canonical_parent.clyphx_pro_component
                data = self._song.get_data(DATA_HEADER % ident, None)
                if data:
                    comp.trigger_action_list('[%s] recall' % ident)
                    self.tpl.log('Recalling snap %s' % ident)
                else:
                    self.tpl.log('No data, cant recall snap %s' % ident)
        except BaseException as e:
            self.tpl.log('ERROR: ' + str(e))

    def on_selected_track_changed(self):
        self.tpl.on_selected_track_changed()
    
    def on_selected_scene_changed(self):
        self.tpl.on_selected_scene_changed()
