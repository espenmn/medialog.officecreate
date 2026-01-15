# -*- coding: utf-8 -*-

from medialog.officecreate import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider
# from plone.autoform import directives
# from plone.app.dexterity.behaviors.metadata import ICategorization


class ISubjectMoverMarker(Interface):
    pass


@provider(IFormFieldProvider)
class ISubjectMover(model.Schema):
    """
    """
    
    template_for  = schema.Tuple(
        title=_(u'Content Type'),
        required=False,
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.PortalTypes",
        ),
    )
   

@implementer(ISubjectMover)
@adapter(ISubjectMoverMarker)
class SubjectMover(object):
    def __init__(self, context):
        self.context = context

    @property
    def template_for(self):
        if safe_hasattr(self.context, 'template_for'):
            return self.context.template_for
        return None

    @template_for.setter
    def template_for(self, value):
        self.context.template_for = value
