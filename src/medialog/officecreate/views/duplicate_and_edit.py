# -*- coding: utf-8 -*-

# from medialog.officecreate import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from plone import api
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from zope.container.interfaces import INameChooser

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IDuplicateAndEdit(Interface):
    """ Marker Interface for IDuplicateAndEdit"""


@implementer(IDuplicateAndEdit)
class DuplicateAndEdit(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('duplicate_and_edit.pt')

    # def __call__(self):
    #     # Implement your own actions:
    #     return self.index()

    def __call__(self):
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)

        new_title = request.get("new_title")
        if not new_title:
            return "Missing new_title"

        context = self.context
        parent = context.aq_parent
        
        oid = INameChooser(parent).chooseName(new_title, context)

        new_obj = api.content.copy(
            source=context,
            target=parent,
             id=oid, 
             safe_id=True
        )
        
        # new_obj.title = new_title
        new_obj.setTitle(new_title)
        new_obj.reindexObject()
        
        return request.response.redirect(
            new_obj.absolute_url() + "/@@edit"
        )
