# -*- coding: utf-8 -*-

from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface
from plone.autoform import directives
from plone.supermodel import model
 
# from Products.CMFPlone.utils import safe_hasattr
# from plone.app.contenttypes import _
# _ = MessageFactory('medialog.officecreate')

class INameValueRow(model.Schema):
    name  = schema.TextLine(title=u"Name", required=False)
    value = schema.TextLine(title=u"Value", required=False)
    
class IMedialogOfficecreateLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""