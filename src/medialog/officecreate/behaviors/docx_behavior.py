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


class IDocxBehaviorMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IDocxBehavior(model.Schema):
    """
    """

    # project = schema.TextLine(
    #     title=_(u'Project'),
    #     description=_(u'Give in a project name'),
    #     required=False,
    # )


@implementer(IDocxBehavior)
@adapter(IDocxBehaviorMarker)
class DocxBehavior(object):
    def __init__(self, context):
        self.context = context

    # @property
    # def project(self):
    #     if safe_hasattr(self.context, 'project'):
    #         return self.context.project
    #     return None

    # @project.setter
    # def project(self, value):
    #     self.context.project = value
