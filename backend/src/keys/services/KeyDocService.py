import locale
import os
from datetime import datetime
import subprocess
from django.template.loader import render_to_string

from ..models.keydoc import KeyDoc
from django.contrib.auth import get_user_model
from django.template.loaders.filesystem import Loader

from django.conf import settings
from unidecode import unidecode


class KeyDocService:
    def __init__(self, model):
        self.keydoc = model

    def decode_ascii(self, value):
        return unidecode(value)

    def generate_file(self):
        template_location = settings.KEYS_TEMPLATE_DIR
        image_location = template_location + "rz_banner.png"

        locale.setlocale(locale.LC_TIME, "pt_PT.utf8")
        today = datetime.now().strftime("%A, %d %B %Y").title()

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
        context = {
            "image": image_location,
            "date": today,
            "signature_space": signature_space,
            "signature": signature,
            "list": members_list_str,
        }
        final_md = render_to_string(settings.KEYDOC_MD, context)

        output_dir = os.getcwd() + "/keys/generated/"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        with open(output_dir + "latest_keydoc.md", "w") as md:
            md.write(final_md)

        subprocess.run(
            ["pandoc", output_dir + "latest_keydoc.md", "-o", output_dir + "latest_keydoc.pdf", "--pdf-engine=xelatex",
             "--template",
             template_location + "eisvogel.tex"])

        self.keydoc.doc = output_dir + "latest_keydoc.pdf"
        self.keydoc.save()
        return self.keydoc.doc