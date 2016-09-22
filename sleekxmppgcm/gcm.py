
MSG = '<message><gcm xmlns="google:mobile:data">{0}</gcm></message>'


class GCMMessageType(object):
    ACK = 'ack'
    NACK = 'nack'
    CONTROL = 'control'
    RECEIPT = 'receipt'

class GCMEvent(object):
    GCM_RECV = 'GCMMessageRECV'

class GCMMessage(ElementBase):
    name = 'gcm'
    namespace = 'google:mobile:data'
    plugin_attrib = 'gcm'
    interfaces = set('json_data')
    sub_interfaces = interfaces
    data = {}

    def __init__(self, xml, parent):
        ElementBase.__init__(self, xml, parent)
        json_str = xml.text
        self.data = json.loads(json_str)

    @property
    def is_error(self):
        if 'error' in self.data.keys():
            return True
        return False

    @property
    def error_description(self):
        if 'error_description' in self.data.keys():
            if self.data.get('error_description') != '':
                return ' %s: %s' % (self.data.get('error', ''), self.data.get('error_description', ''))
            else:
                return self.data.get('error')
        return ''

    @property
    def message_id(self):
        return self.data.get('message_id', '')

    @property
    def message_type(self):
        return self.data.get('message_type', '')


class GCMClient(ClientXMPP):

    def __init__(self, id, password):
        ClientXMPP.__init__(self, id, password, sasl_mech='PLAIN')
        self.event_processor = GCMMessageProcessor()

        register_stanza_plugin(Message, GCMMessage)

        self.register_handler(
            Callback('GCM Message', StanzaPath('message/gcm'), self.on_gcm_message)
        )

        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler(GCMEvent.GCM_RECV, self.event_processor.on_ack, threaded=True)

    def on_gcm_message(self, msg):
        self.event(GCMEvent.GCM_RECV, msg['gcm'])

    def session_start(self, event):
        print "Session Start"
        self.send_gcm()

    def send_gcm(self):
        self.send_raw(MSG)


class GCMMessageProcessor():

    def __init__(self):
        pass

    def on_ack(self, msg):
        #  # run the even on another thread.
        if msg.message_type == GCMMessageType.NACK:
            logging.debug('Received NACK for message_id: %s with error, %s' % (msg.message_id, msg.error_description))

        elif msg.message_type == GCMMessageType.ACK:
            logging.debug('Received ACK for message_id: %s' % msg.message_id)
            logging.debug('Msg: %s' % json.dumps(msg))

