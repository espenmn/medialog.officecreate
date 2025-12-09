# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase


class OfficeCreateViewlet(ViewletBase):

    def update(self):
        self.message = self.get_message()

    def get_message(self):
        return self.context.absolute_url()
    
    def index(self):
        return super(OfficeCreateViewlet, self).render()



