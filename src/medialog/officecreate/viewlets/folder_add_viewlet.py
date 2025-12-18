# -*- coding: utf-8 -*-

from zope.component import getMultiAdapter
from plone.app.layout.viewlets import ViewletBase


class FolderAddViewlet(ViewletBase):

    def update(self):
        self.message = self.get_message()
        
    def get_message(self):
        return self.context.absolute_url()
    
    def index(self):
        return super(FolderAddViewlet, self).render()



