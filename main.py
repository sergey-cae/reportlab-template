from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.tables import Table, TableStyle, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import inch, cm
from reportlab.lib.utils import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.lib import utils

imagelist = sorted([f"{img_folder_updated}/{i}" for i in os.listdir(img_folder_updated) if i.endswith('.png') or i.endswith('.json')])
# imagelist = sorted([f"{img_folder}/{i}" for i in os.listdir(img_folder) if i.endswith('.svg')])

class ChartDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [Frame(2.5*cm, 2.5*cm, 16*cm, 26*cm, id='F1')])
        self.addPageTemplates(template)
    
    def afterFlowable(self, flowable):
        """Registers TOC entries."""
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name

            if style == 'Head1':
                key = 'h1-%s' % self.seq.nextf('head1')
                self.canv.bookmarkPage(key, fit="XYZ", top=850, zoom=0)
                if text != "Content":
                    self.notify('TOCEntry', (0, text, self.page, key))
                    self.addOutlineEntry(text, key, 0, 0)

            if style == 'Head2':
                key = 'h2-%s' % self.seq.nextf('head2')
                self.canv.bookmarkPage(key, fit="XYZ", top=850, zoom=0)
                self.notify('TOCEntry', (1, text, self.page, key))
                self.addOutlineEntry(text, key, 1, 1)


            if style == 'Head3':
                key = 'h3-%s' % self.seq.nextf('head3')
                self.canv.bookmarkPage(key, fit="XYZ", top=850, zoom=0)
                self.notify('TOCEntry', (2, text, self.page, key))
                self.addOutlineEntry(text, key, 2, 2)

            if style == 'Head4':
                key = 'h4-%s' % self.seq.nextf('head4')
                print(key)
                self.canv.bookmarkPage(key, fit="XYZ", top=850, zoom=0)
                # self.notify('TOCEntry', (3, text, self.page, key)) # uncomment if need it in TOC
                self.addOutlineEntry(text, key, 3, 1)

def get_image(path, width=1*cm):
    if path.endswith('-json'):
        err_obj = json.load(open(path))

        img = {
            "image": path.split('$')[-1].split('.')[0],
            "type": err_obj['type'],
            "message": err_obj['url']
        }

        return [
            Paragraph(img["image"], h5),
            Paragraph(img["type"], p1),
            Paragraph(img["message"], p1)
        ]
    else:
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect))
        # return svg2rlg(path)



chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                          ('VALIGN', (0, 0), (-1, -1), 'CENTER')])


def is_int(n):
    try:
        int(n)
        return True
    except:
        return False


def layout_images(imagelist, l=3):
    skip = False
    for i in range(len(imagelist)):
        if skip:
            skip = False
            continue

        pic1 = imagelist[i]
        row1 = imagelist[i].split('$$')[1].split('.')[0]
        col1 = imagelist[i].split('$$')[1].split('.')[1]

        if i + 1 < len(imagelist):
            pic2 = imagelist[i + 1]
            row2 = imagelist[i + 1].split('$$')[1].split('.')[0]
            col2 = imagelist[i + 1].split('$$')[1].split('.')[1]
        else:
            row2 = ""

        im1 = get_image(pic1, width=3.8*inch)

        if row1 == row2:
            # Create 2 images row
            im2 = get_image(pic2, width=3.8*inch)

            layout.append(Table([[im1, im2]],
                                colWidths=[3.8 * inch, 3.8 * inch],
                                # rowHeights=[2.5 * inch], style=chart_style))
                                style=chart_style))

            print("2 images", pic1.split('$$')[1], pic2.split('$$')[1])
            skip = True
        else:
            # Create 1 image row
            layout.append(Table([[im1]],
                                colWidths=[3.8 * inch],
                                # rowHeights=[2.5 * inch], style=chart_style))
                                style=chart_style))

            print("1 image", pic1.split('$$')[1])

    layout.append(Spacer(1, 12))
    return layout


styles = getSampleStyleSheet()

h1 = PS(
    name="Head1",
    parent=styles["Heading1"],
    alignment=1,
    fontSize=16,
    textColor=HexColor(0xff8100),
    textColor=HexColor(0xcc6600),
    leading=18,
    spaceBefore=0,
    spaceAfter=0,
)

h2 = PS(
    name="Head2",
    parent=styles["Heading2"],
    alignment=1,
    fontSize=14,
    leftIndent=12,
    textColor=HexColor(0x006600),
    leading=16,
    spaceBefore=0,
    spaceAfter=0,
)

h3 = PS(
    name="Head3",
    parent=styles["Heading3"],
    fontSize=12,
    leftIndent=24,
    textColor=HexColor(0x000099),
    leading=14,
    spaceBefore=0,
    spaceAfter=0,
)


h4 = PS(
    name="Head4",
    fontName="Helvetica-Bold",
    parent=styles["Heading4"],
    fontSize=10,
    leftIndent=36,
    textColor=HexColor(0x333333),
    leading=12,
    spaceBefore=0,
    spaceAfter=0,
)

h5 = PS(
    name="Head5",
    parent=styles["Heading5"],
    fontSize=10,
    leftIndent=0,
    # textColor=HexColor(0x000000),
    leading=12,
    spaceBefore=0,
    spaceAfter=0,
)

p1 = PS(
    name="P4",
    parent=styles["Normal"],
    # fontSize=12,
    leftIndent=0,
    # textColor=HexColor(0x000000),
    # leading=14,
    spaceBefore=0,
    spaceAfter=0,
)

# Build layout.
layout = []
toc = TableOfContents()
# For conciseness, we use the same styles for headings and TOC entries
toc.levelStyles = [h1, h2, h3, h4]

layout.append(Paragraph("Content", h1))
layout.append(toc)
layout.append(PageBreak())

for section in sorted(set([i.split('$$')[0] for i in imagelist])):
    imagelist_sec = sorted([i for i in imagelist if i.startswith(section)])
    countries = sorted(set([i.split('$$')[1] for i in imagelist if i.startswith(section)]))

    layout.append(Paragraph(section.split('/')[-1], h1))
    layout.append(Spacer(1, 12))

    for country in countries:
        imagelist_country = sorted([i for i in imagelist_sec if i.startswith(f"{section}$${country}")])
        country_root_images = [i for i in imagelist_country if is_int(i.split('$$')[2][1:3])]

        categories = sorted(set([i.split('$$')[2] for i in imagelist_sec if i.startswith(f"{section}$${country}")]))
        categories_dict = dict.fromkeys(sorted(set([c.split(' - ')[0] for c in categories])))
        categories_dict = {c: sorted(set([i.split('$$')[2].split(' - ')[-1] for i in imagelist_sec if i.startswith(f"{section}$${country}$${c} - ")])) for c in categories_dict}

        layout.append(Paragraph(country, h2))
        layout.append(Spacer(1, 12))

        if len(country_root_images) > 0:
            layout_images(country_root_images, 2)
            layout.append(Spacer(1, 12))


    for category in categories_dict:
        if len(categories_dict[category]) == 0:
            imagelist_category = sorted(set([i for i in imagelist_sec if i.startswith(f"{section}$$${country}$$${category}")]))
            print(section, country, category)

            if not is_int(category[1:3]):
                # layout.append(Paragraph(f"River of Knowledge ({category})", styles["Heading3"]))
                layout.append(Paragraph(category, h3))
                layout.append(Spacer(1, 12))
                layout_images(imagelist_category, 2)
                layout.append(Spacer(1, 12))

                layout.append(PageBreak())
            else:
                layout.append(Paragraph(category, h3))
                layout.append(Spacer(1, 12))
        else:
            layout.append(Paragraph(category, h3))
            layout.append(Spacer(1, 12))

            last_subcat = categories_dict[category][-1]
            add_spacer = False
            for subcat in categories_dict[category]:
                imagelist_category = sorted(set([i for i in imagelist_sec if i.startswith(f"{section}$$${country}$$${category} - {subcat}")]))
                print(section, country, category, subcat)

                layout.append(Paragraph(subcat, h4))
                layout.append(Spacer(1, 12))
                layout_images(imagelist_category, 2)
                layout.append(Spacer(1, 12))

                if len(imagelist_category) > 2 or subcat == last_subcat or add_spacer:
                    layout.append(PageBreak())
                    add_spacer = False
                else:
                    add_spacer = True


doc = ChartDocTemplate(f"/usr/local/airflow/rok/charts_{str(datetime.now())[:10]}.pdf")
doc.multiBuild(layout)

# END REPORTLAB SCRIPT

# GENERATE EMAIL BODY
d = prev_folder.split('_')[-1]

print("Chart Summary:", f"{d[:4]}-{d[4:6]}-{d[6:]} .. {str(datetime.now())[:10]}")
print(f"Total charts: len(pngs)+len(svgs)")
print(f"Macrodb: len(macrodbs)+len(wrong_links)+len(s3_errors)")

# GENERATE EMAIL BODY
d = prev_folder.split('_')[-1]

print("Chart Summary:", f"{d[:4]}-{d[4:6]}-{d[6:]} .. {str(datetime.now())[:10]}")
print(f"\tTotal charts: ", len(pngs) + len(svgs))
print(f"\tMacrodb: ", len(macrodbs) + len(wrong_links) + len(s3_errors))

print(f"\t\tSignificant Changes: ", len(really_diff))
print(f"\t\tMissing: ", len(wrong_links) + len(s3_errors))

print(f"\t\tSharepoint: ", len(sharepoints))
print(f"\t\tUpdated: ", len(sharepoints) - len(set(sharepoints) - set(updated_images)))
print(f"\t\tMissing: ", len(sharepoint_urls))
print(f"\t\tStale: ", len(set(sharepoints) - set(updated_images)) - len(sharepoint_urls))

print()
print(f"F-on-W Significant Changes (threshold = {threshold}):")
print()

for i in really_diff:
    country = i.split('$$')[1]
    category = i.split('$$')[2]
    id = i.split('$$')[4].split('.')[0]
    pos = i.split('$$')[3].replace('r', 'row ').replace('c', 'column ').replace('0', '.').replace(',', '.')
    print(f"\t{country} - {category} - {pos} - {id}")
