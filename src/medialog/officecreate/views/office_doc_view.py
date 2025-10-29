# -*- coding: utf-8 -*-

# from medialog.officecreate import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from plone.namedfile.file import NamedBlobImage
from plone.app.textfield.value import RichTextValue
from html2docx import html2docx
from plone.app.querystring import queryparser
#from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import iterSchemata
from zope.schema import getFieldsInOrder
from plone import api

# import docx
from docx import Document
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage, RichText
from io import BytesIO

class IOfficeDocView(Interface):
    """ Marker Interface for IOfficeDocView"""


@implementer(IOfficeDocView)
class OfficeDocView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('office_doc_view.pt')

    def __call__(self):
        context = self.context
        selected_file_id = self.request.form.get('selected_file', None)
        # files = self.find_docx_in_templates()
        # If no file is found or user hasn't selected one, render a form to choose a file
        if not selected_file_id:
            return self.index()

        if selected_file_id:
            # Extract the selected file's data
            filen = api.content.get(UID=selected_file_id)
            file_data = filen.file.data
            
            # Wrap in BytesIO for docxtpl etc
            file_stream = BytesIO(file_data)
            doc = DocxTemplate(file_stream)

            # Get context data for replacements
            replacements = self.get_replacements(context, doc)
            doc.render(replacements)

            # Prepare the output file stream for download
            output_stream = BytesIO()
            doc.save(output_stream)
            output_stream.seek(0)

            # Return the generated document as a downloadable response
            self.request.response.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            self.request.response.setHeader('Content-Disposition', 'attachment; filename="generated.docx"')

            return output_stream.getvalue()

        return "No valid file selected."
    
    def get_replacements(self, context, doc):
        """Get the replacements for the Word template."""
        replacements = {}
        
        
        for schema in iterSchemata(context):
            schema_obj = schema(context)  # This adapts context to the schema
            for name, field in getFieldsInOrder(schema):
                value = getattr(schema_obj, name, None)
                if value: 
                    description = getattr(schema_obj, name, None)
                    if isinstance(value, NamedBlobImage) and getattr(value, 'data', None):
                        # Handle image field
                        field_description = int(field.description)
                        image_stream = BytesIO(value.data)
                        replacements[name] = InlineImage(doc, image_stream, width=Mm(field_description))
                    if isinstance(value, RichTextValue) and getattr(value, 'output', None):
                        html = value.raw
                        subdoc_stream = BytesIO()
                        #document = Document()
                        document = Document()
                        html2docx(html, document)
                        document.save(subdoc_stream)
                        subdoc_stream.seek(0)
                        subdoc = Document().new_subdoc(subdoc_stream)
                        replacements[name] = subdoc
                    else:
                        # Normal field
                        replacements[name] = value
                    
        replacements['title'] = context.Title()
        replacements['description'] = context.Description()
        
        # image_field = getattr(context, 'myfield', None)
        # if image_field and getattr(image_field, 'data', None):
        #     image_data = image_field.data
        #     image_stream = BytesIO(image_data)
        #     # Use InlineImage from docxtpl
        #     replacements['myimage'] = InlineImage(doc, image_stream, width=Mm(50))  # adjust size

        
        return replacements
    
        
    def find_docx_in_templates(self):
        # Define the path to search within (e.g., /templates)
        folder_path = 'Plone11/templates'
        
        # Search for all File content items within the folder
        documents = api.content.find(portal_type='File', path={'query': folder_path, 'depth': 1})
        
        # Collect the items
        docx_items = []
        for document in documents: 
            obj = document.getObject()
            file_type = obj.file.contentType
            if file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                docx_items.append({
                    'title': obj.Title(),
                    # 'url': obj.absolute_url, 
                    # 'object': obj,
                    'uuid': obj.UID(),
                    'file_name': obj.file.filename  # Include the filename as well for easier reference
                })
        
        return docx_items