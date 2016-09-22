"""
    SleekXMPPGCM: XMPP Client for Google/Firebase Cloud Messaaging
    Copyright (C) 2016  Winster Jose
    This file is part of SleekXMPPGCM.

    See the file LICENSE for copying permission.
"""

import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.xmlstream.stanzabase import ElementBase
from sleekxmpp.stanza import Message
from sleekxmpp.xmlstream import register_stanza_plugin
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher import StanzaPath
import uuid
import json