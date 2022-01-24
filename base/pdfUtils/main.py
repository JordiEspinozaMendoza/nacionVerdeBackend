from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
import os


def createPdf(name, qty):
    try:
        module_dir = os.path.dirname(__file__)
        sacramentoPath = os.path.join(module_dir, "Sacramento.ttf")
        poppinsPath = os.path.join(module_dir, "Poppins-Bold.ttf")
        pdfmetrics.registerFont(TTFont("Sacramento", sacramentoPath))
        pdfmetrics.registerFont(TTFont("Poppins-Bold", poppinsPath))
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Sacramento", 40)

        if len(str(name)) > 20:
            can.drawString(140, 250, name)
        else:
            can.drawString(210, 250, name)

        can.setFillColor(HexColor("#508152"))
        can.setFont("Poppins-Bold", 60)

        if len(str(qty)) == 1:
            can.drawString(295, 330, f"{qty}")
        else:
            can.drawString(280, 330, f"{qty}")

        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)

        # create a new PDF with Reportlab
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        if qty == 1:
            existing_pdf_path = os.path.join(module_dir, "tree.pdf")
        else:
            existing_pdf_path = os.path.join(module_dir, "trees.pdf")
        existing_pdf = PdfFileReader(open(existing_pdf_path, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStreamPath = os.path.join(module_dir, f"{name}.pdf")
        outputStream = open(outputStreamPath, "wb")
        output.write(outputStream)
        outputStream.close()

        # Now we have to return the pdf
        return outputStreamPath
    except Exception as e:
        print(str(e))
