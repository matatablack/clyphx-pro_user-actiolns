
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from utils.log_utils import dumpobj


class TemplateDisplayerActions(UserActionsBase):

    def create_actions(self):
        self.add_global_action('show_control_mode', self.show_control_mode)
        self.add_global_action('show_msg', self.show_msg)

    def show_control_mode(self, action_def, args):
        try:
            self.canonical_parent.log_message('-----show control mode-----')
            self.canonical_parent.log_message('message %s' % args)
            dictionary = {'message': args}
            actions = '''OSC STR custom/global/control_mode {message};'''.format(**dictionary)
            self.canonical_parent.log_message(actions)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    def show_msg(self, action_def, args):
        try:
            self.canonical_parent.log_message(
                '-----show_message-----')
            self.canonical_parent.log_message('message %s' % args)
            args = args.split('"')
            autoclean = False if args[2] and args[2].strip(
            ) == "off" else True
            dictionary = {'message': args[1]}
            actions = '''
                OSC STR custom/global/msg "{message}";
            '''.format(**dictionary)
            self.canonical_parent.log_message(actions)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                actions)

            # if autoclean:
            #     autoclean_actions = '''
            #         WAIT 20;
            #         OSC STR custom/global/msg "---";
            #     '''.format(**dictionary)

            #     self.canonical_parent.log_message(autoclean_actions)
            #     self.canonical_parent.clyphx_pro_component.trigger_action_list(autoclean_actions)

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))