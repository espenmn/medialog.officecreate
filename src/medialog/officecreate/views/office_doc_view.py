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
from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate, InlineImage, RichText

import tempfile
import os



#For PowerPoint:
from pptx import Presentation
from io import BytesIO

from PIL import Image

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
        
            # --- 1. Get Text/Simple Replacements ---
            # Assuming get_doc_replacements() returns a dictionary of simple variables
            replacements = self.get_doc_replacements(context, doc)
            
            # --- 2. Add Image Replacements to the SAME Dictionary ---
            for schema in iterSchemata(context):
                schema_obj = schema(context)
                for name, field in getFieldsInOrder(schema):
                    value = getattr(schema_obj, name, None)
                    
                    if isinstance(value, NamedBlobImage) and getattr(value, 'data', None):
                        image_stream = BytesIO(value.data)
                        alt_text_identifier = name 

                        # *** IMPORTANT: replace_pic needs a file path, not a stream ***
                        # We must write the stream to a temporary file in Plone/Python
                        suffix = os.path.splitext(value.filename)[1]
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_img_file:
                            temp_img_file.write(value.data)
                            temp_img_path = temp_img_file.name 

                        # This method should fill the existing shape size in the template
                        doc.replace_media(alt_text_identifier, temp_img_path)
                        
                        # width = shape.width or Mm(default_size_mm)
                        # height = shape.height or Mm(default_size_mm)
                        # Note: You can skip the EMU calculation unless you need exact pixel sizing
                        # docxtpl handles sizing well with Mm or Inches classes
                        
                        # Add the InlineImage object to the main replacements dictionary.
                        # The 'name' variable here is assumed to be the FIELD NAME in Plone, 
                        # which should match the JINJA2 TAG in your DOCX template (e.g., {{ name }} )
                        replacements[name] = InlineImage(doc, image_stream, width=Mm(50))

            # --- 3. RENDER ONCE with the complete dictionary ---
            doc.render(replacements)

            # --- 4. Save and return the file (Plone specific handling) ---
            # Use a BytesIO object to capture the output for Plone response
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
            replacements = self.get_ppt_replacements(context, prs)
            
            for slide in prs.slides:
                for shape in slide.shapes:
                    
                    if shape.shape_type == 13:  # 13 means it's a picture
                        # Use image alt text for key
                        key = shape.image._filename.split('.')[0]
                        
                        if  hasattr(context, key):
                            img_obj = getattr(context, key, None)
                            
                            # must have .data                            
                            if getattr(img_obj, "data", None):
                                image_stream = BytesIO(img_obj.data)
                                
                                # Placeholder
                                left = shape.left
                                top = shape.top
                                width = shape.width
                                height = shape.height

                                # Load image
                                image_stream.seek(0)
                                pil_img = Image.open(image_stream)
                                img_w, img_h = pil_img.size  # px

                                # Convert EMU → px
                                EMU_PER_INCH = 914400
                                PX_PER_INCH = 96
                                frame_w_px = width / EMU_PER_INCH * PX_PER_INCH
                                frame_h_px = height / EMU_PER_INCH * PX_PER_INCH

                                # Scale to COVER
                                scale = max(frame_w_px / img_w, frame_h_px / img_h)
                                new_w_px = img_w * scale
                                new_h_px = img_h * scale

                                # Convert back to EMU
                                new_width = int(new_w_px / PX_PER_INCH * EMU_PER_INCH)
                                new_height = int(new_h_px / PX_PER_INCH * EMU_PER_INCH)

                                # Remove old picture
                                sp = shape._element
                                sp.getparent().remove(sp)

                                image_stream.seek(0)

                                # Add new picture at full scaled size (cover)
                                new_shape = shape.part.slide.shapes.add_picture(
                                    image_stream,
                                    left,
                                    top,
                                    width=width,
                                    height=height
                                )

                                # ---- Crop to match original placeholder ----
                                # Calculate crop ratios (0-1)
                                crop_left = max((new_width - width) / 2 / new_width, 0)
                                crop_top  = max((new_height - height) / 2 / new_height, 0)
                                crop_right = crop_left
                                crop_bottom = crop_top

                                # Apply cropping
                                new_shape.crop_left = crop_left
                                new_shape.crop_top = crop_top
                                new_shape.crop_right = crop_right
                                new_shape.crop_bottom = crop_bottom
                    
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
    
    
    def get_doc_replacements(self, context, doc):
        """Get the replacements for the Word template."""
        replacements = {}        
        
        for schema in iterSchemata(context):
            schema_obj = schema(context)  # This adapts context to the schema
            for name, field in getFieldsInOrder(schema):
                value = getattr(schema_obj, name, None)
                if not value:
                    continue
                if isinstance(value, NamedBlobImage) and getattr(value, 'data', None):
                    continue                           
                            
                # if isinstance(value, RichTextValue) and getattr(value, 'output', None):
                #     html = value.raw
                #     subdoc_stream = BytesIO()
                #     #document = Document()
                #     document = Document()
                #     html2docx(html, document)
                #     document.save(subdoc_stream)
                #     subdoc_stream.seek(0)
                #     subdoc = Document().new_subdoc(subdoc_stream)
                #     replacements[name] = subdoc
                else:
                    # Normal field
                    replacements[name] = value
                    
        replacements['title'] = context.Title()
        replacements['description'] = context.Description()
        
        return replacements
    
    def get_ppt_replacements(self, context, doc):
        """Get the replacements for the PPT template."""
        replacements = {}        
        
        for schema in iterSchemata(context):
            schema_obj = schema(context)  # This adapts context to the schema
            for name, field in getFieldsInOrder(schema):
                value = getattr(schema_obj, name, None)
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
        