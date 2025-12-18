# -*- coding: utf-8 -*-

from zope.component import getMultiAdapter
from plone.app.layout.viewlets import ViewletBase


class FolderAddViewlet(ViewletBase):

    def update(self):
        super().update()
        self.message = self.get_message()
        request = self.request
        context = self.context
        view = self.view

        # This is the same menu used by the toolbar
        menu = getMultiAdapter(
            (context, request, view),
            name="plone_contentmenu_factory"
        )

        self.add_menu_items = menu.getMenuItems(context, request)

    def get_message(self):
        return self.context.absolute_url()
    
    # def index(self):
    #     return super(FolderAddViewlet, self).render()



