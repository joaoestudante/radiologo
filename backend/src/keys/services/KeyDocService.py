import locale
import os
import hashlib
from datetime import datetime
import subprocess

from django.db import transaction
from django.template.loader import render_to_string

from exceptions.radiologoexception import NoNewMembersForKeyDocException
from ..models.keydoc import KeyDoc
from django.contrib.auth import get_user_model
from django.template.loaders.filesystem import Loader

from django.conf import settings
from unidecode import unidecode


class KeyDocService:
    def __init__(self, user):
        self.keydoc = None
        self.user = user

    def decode_ascii(self, value):
        return unidecode(value)

    @transaction.atomic
    def generate_file(self):
        try:
            previous_doc = KeyDoc.objects.latest('pk')
        except KeyDoc.DoesNotExist:
            previous_doc = None
        self.keydoc = KeyDoc(creator=self.user, members_when_created=get_user_model().objects.count())

        self.checkNeedsGeneration(previous_doc, self.keydoc)
        context = self.build_context()
        final_md = render_to_string(settings.KEYDOC_MD, context)
        pdf_location = self.build_pdf(final_md)

        with open(pdf_location, "rb") as pdf:
            pdf_hash = hashlib.sha256(pdf.read()).hexdigest()
        self.keydoc.doc_hash = pdf_hash
        self.keydoc.save()

        return pdf_location

    def build_context(self) -> dict:
        image_location = settings.KEYS_TEMPLATE_DIR + "rz_banner.png"
        #locale.setlocale(locale.LC_TIME, "pt_PT.utf8")
        #today = datetime.now().strftime("%A, %d %B %Y").title()
        today = datetime.now().strftime("%d-%m-%Y")
        signature = "{} ({}, {})".format(self.keydoc.creator.author_name, self.keydoc.creator.phone,
                                         self.keydoc.creator.email)
        signature_space = "_" * len(signature)

        members_list = []
        for user in get_user_model().objects.all().order_by('author_name'):
            if user.ist_student_options == "Y" or user.ist_student_options == "N":
                if user.ist_student_number is None:
                    ist_number = "Desconhecido"
                else:
                    ist_number = user.ist_student_number
            else:
                ist_number = "Externo"

            if user.id_type == "CC":
                id_number = user.id_number
            else:
                id_number = "{} ({})".format(user.id_number, user.get_id_type_display())

            members_list.append("|{}|{}|{}|\n".format(user.author_name, id_number, ist_number))
        members_list_str = "".join(members_list)

        return {
            "image": image_location,
            "date": today,
            "signature_space": signature_space,
            "signature": signature,
            "list": members_list_str,
        }

    def build_pdf(self, final_md):
        output_dir = os.getcwd() + "/keys/generated/"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        with open(output_dir + "latest_keydoc.md", "w") as md:
            md.write(final_md)
        subprocess.run(
            ["pandoc", output_dir + "latest_keydoc.md", "-o", output_dir + "latest_keydoc.pdf", "--pdf-engine=xelatex",
             "--template",
             settings.KEYS_TEMPLATE_DIR  + "eisvogel.tex"])
        return output_dir + "latest_keydoc.pdf"

    def checkNeedsGeneration(self, previous_doc, new_doc):
        if previous_doc is None:
            # Never generated a PDF, safe to go
            return
        if previous_doc.members_when_created == new_doc.members_when_created:
            raise NoNewMembersForKeyDocException
        else:
            return
