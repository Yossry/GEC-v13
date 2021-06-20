from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

import io
import xml.dom.minidom
from xml.dom.minidom import parseString
import zipfile
from os import listdir
import qrcode
import base64
from io import BytesIO


class QrCodeAccountMove(models.Model):
    _inherit = 'account.move'

    qr_code = fields.Binary("QR Code", attachment=True, store=True)

    def l10n_co_edi_download_electronic_invoice(self):
        if self.type in ['in_refund', 'in_invoice']:
            raise UserError(_(
                'You can not Download Electronic Invoice for Vendor Bill and '
                'Vendor Credit Note.'))

        invoice_download_msg, attachments = super(QrCodeAccountMove,
                                                  self).l10n_co_edi_download_electronic_invoice()
        if attachments:
            with tools.osutil.tempdir() as file_dir:
                zip_ref = zipfile.ZipFile(io.BytesIO(attachments[0][1]))
                zip_ref.extractall(file_dir)
                xml_file = [f for f in listdir(file_dir) if f.endswith('.xml')]
                if xml_file:
                    content = xml.dom.minidom.parseString(
                        zip_ref.read(xml_file[0]))
                    element = content.getElementsByTagName('cbc:UUID')
                    description = content.getElementsByTagName(
                        'cbc:Description')
                    if element:
                        self.l10n_co_edi_cufe_cude_ref = element[0].childNodes[0].nodeValue
                    if description:
                        desc = description[0].childNodes[0].nodeValue
                        convert_desc = parseString(desc)
                        tag_xml = convert_desc.getElementsByTagName('cbc:Note')
                        if tag_xml:
                            qr_txt = tag_xml[9].childNodes[0].nodeValue
                            qr_lst = qr_txt.split()
                            text = self.split(qr_lst, 2)
                            self.create_qr_code(text)

        return invoice_download_msg, attachments

    def split(self, arr, size):
        arrs = []
        arrs_set = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr = arr[size:]
        arrs.append(arr)

        for i in arrs:
            str_qr = ' '.join(i)
            arrs_set.append(str_qr)
        tx = ''
        for ar in arrs_set:
            tx += ar + '\n'
        return tx


    def create_qr_code(self, text):
        qr = qrcode.QRCode(version=4,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=4, border=4, )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_code = qr_image
