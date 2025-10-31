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

#For PowerPoint:
from pptx import Presentation
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

        if not selected_file_id:
            return self.index()

        filen = api.content.get(UID=selected_file_id)
        if not filen or not hasattr(filen, 'file'):
            return "Invalid file selected."

        file_data = filen.file.data
        file_stream = BytesIO(file_data)

        # Determine file type
        portal_type = getattr(filen, 'portal_type', '').lower()

        # Handle DOCX (Word)
        if portal_type in ('file', 'document') and filen.file.filename.endswith('.docx'):
            doc = DocxTemplate(file_stream)
            replacements = self.get_replacements(context, doc)
            doc.render(replacements)

            output_stream = BytesIO()
            doc.save(output_stream)
            output_stream.seek(0)

            self.request.response.setHeader(
                'Content-Type',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            self.request.response.setHeader(
                'Content-Disposition',
                'attachment; filename="generated.docx"'
            )

            return output_stream.getvalue()

        # Handle PPTX (PowerPoint)
        elif portal_type in ('file', 'presentation') or filen.file.filename.endswith('.pptx'):
            prs = Presentation(file_stream)
            replacements = self.get_replacements(context, prs)
            
            for slide in prs.slides:
                for shape in slide.shapes:
                    if not shape.has_text_frame:
                        continue

                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                                original_text = run.text
                                new_text = original_text
                                for key, value in replacements.items():
                                    # import pdb; pdb.set_trace()
                                    strvalue = str(value).replace("\r", "")
                                    #.replace("\n", "*")
                                    new_text = new_text.replace(key, strvalue)
                                    
                                if new_text != original_text:
                                    run.text = new_text
                            
            output_stream = BytesIO()
            prs.save(output_stream)
            output_stream.seek(0)

            self.request.response.setHeader(
                'Content-Type',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            )
            self.request.response.setHeader(
                'Content-Disposition',
                'attachment; filename="generated.pptx"'
            )

            return output_stream.getvalue()

        return "Unsupported or invalid file type."
    
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
        
        return replacements
    
        
    def find_docx_in_templates(self):
        # Define the path to search within (e.g., /templates)
        portal = api.portal.get()
        docx_items = []
        if portal.get('templates', False):            
            templates = portal.get('templates')
            
            # Search for all File content items within the folder
            documents = api.content.find(
                portal_type='File',
                context=templates,
            )
            
            # Collect the items
            for document in documents: 
                obj = document.getObject()
                file_type = obj.file.contentType
                if file_type in  [
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'application/vnd.openxmlformats-officedocument.presentationml.presentation'
                    ]:
                    docx_items.append({
                        'title': obj.Title(),
                        'file_type': file_type.split('.')[-1],
                        # 'url': obj.absolute_url, 
                        # 'object': obj,
                        'uuid': obj.UID(),
                        'file_name': obj.file.filename  # Include the filename as well for easier reference
                    })
        
        return docx_items
        