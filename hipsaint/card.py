import uuid
from .options import STATE_STYLES, NOTIFICATION_STYLES


ICON_URL = 'http://i.imgur.com/BxqWsDC.png'


class Card(object):
    def __init__(self, inputs, handler_type):
        self.inputs = inputs
        self.handler_type = handler_type
        if handler_type == 'host':
            self.hostname, self.timestamp, self.ntype, self.hostaddress, self.state, self.hostoutput = [
                inp.strip() for inp in self.inputs.split('|')]
        else:
            self.service, self.hostalias, self.timestamp, self.ntype, self.hostaddress, self.state, self.hostoutput = [
                inp.strip() for inp in self.inputs.split('|')]

    def get_style_old(self):
        """
        Style mapping for the supported atlassian lozenge styles.
        For more see: https://docs.atlassian.com/aui/latest/docs/lozenges.html
        """
        state_mapping = {
            'CRITICAL': 'lozenge-error',
            'WARNING': 'lozenge-current',
            'OK': 'lozenge-success',
            'UNKNOWN': 'lozenge',
            'DOWN': 'lozenge-error',
            'UP': 'lozenge-success',
            'UNREACHABLE': 'lozenge-error'
        }

        if self.state not in state_mapping:
            return 'lozenge'
        else:
            return state_mapping[self.state]

    def get_attributes(self):
        """
        More about Card attributes:
        https://developer.atlassian.com/hipchat/guide/sending-messages
        """
        attributes = [
            {
                'value': {
                    'label': self.ntype
                },
                'label': 'Type'
            },
            {
                'value': {
                    'label': self.state,
                    'style': STATE_STYLES.get(self.state, 'lozenge')
                },
                'label': 'State'
            },
            {
                'value': {
                    'label': '%s (%s)' % (self.hostname if self.handler_type == 'host' else
                                          self.hostalias, self.hostaddress)
                },
                'label': 'Host'
            }]
        return attributes

    def get_activity(self):
        """
        More about Card activity:
        https://developer.atlassian.com/hipchat/guide/sending-messages
        """
        if self.handler_type == 'host':
            activity = {
                'html': '<b>%(hostname)s</b> (%(hostaddress)s) - <span class="aui-lozenge aui-%(style)s">%(ntype)s</span>' % {
                    'hostname': self.hostname,
                    'hostaddress': self.hostaddress,
                    'style': NOTIFICATION_STYLES.get(self.ntype, "lozenge"),
                    'ntype': self.ntype},
                'icon': ICON_URL
            }
        else:
            activity = {
                'html': '<b>%(service)s</b> on %(hostalias)s (%(hostaddress)s) - <span class="aui-lozenge aui-%(style)s">%(ntype)s</span>' % {
                    'hostalias': self.hostalias,
                    'service': self.service,
                    'hostaddress': self.hostaddress,
                    'style': NOTIFICATION_STYLES.get(self.ntype, "lozenge"),
                    'ntype': self.ntype},
                'icon': ICON_URL}
        return activity

    def get_card(self):
        card_object = {
            'id': str(uuid.uuid4()),
            'icon': ICON_URL,
            'style': 'application',
            'format': 'medium',
            'title': '',
            'description': self.hostoutput,
            # The box content comes from here:
            'activity': self.get_activity(),
            'attributes': self.get_attributes()
        }
        if self.handler_type == 'host':
            card_object['title'] = '%(ntype)s - %(hostname)s (%(hostaddress)s) is %(state)s' % {
                    'ntype': self.ntype,
                    'hostname': self.hostname,
                    'hostaddress': self.hostaddress,
                    'state': self.state
                }
        else:
            card_object['title'] = '%(ntype)s - %(service)s on %(hostalias)s (%(hostaddress)s) is %(state)s' % {
                    'ntype': self.ntype,
                    'service': self.service,
                    'hostalias': self.hostalias,
                    'hostaddress': self.hostaddress,
                    'state': self.state
                }

        return card_object
