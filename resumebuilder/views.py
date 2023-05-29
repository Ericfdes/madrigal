import textwrap
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.templatetags.static import static
import io
import os

#Libraries for ReportLab
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfdoc
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from resumebuilder.forms import *

# Create your views here.

# Import font
registerFont(TTFont('Inconsolata', os.path.join(settings.BASE_DIR, 'website_hr','static', 'resumebuilder', 'fonts', 'Inconsolata-Regular.ttf')))
registerFont(TTFont('InconsolataBold', os.path.join(settings.BASE_DIR, 'website_hr','static', 'resumebuilder', 'fonts', 'Inconsolata-Bold.ttf')))
registerFont(TTFont('FontAwesome', os.path.join(settings.BASE_DIR, 'website_hr','static', 'resumebuilder', 'fonts', 'fontawesome-webfont.ttf')))
registerFont(TTFont('Poppins', os.path.join(settings.BASE_DIR, 'website_hr','static', 'resumebuilder', 'fonts', 'poppins-regular.ttf')))
registerFont(TTFont('PoppinsBold', os.path.join(settings.BASE_DIR, 'website_hr','static', 'resumebuilder', 'fonts', 'poppins-bold.ttf')))
registerFont(TTFont('PoppinsBoldItalic', os.path.join(settings.BASE_DIR, 'website_hr','static', 'resumebuilder', 'fonts', 'poppins-bold-italic.ttf')))
registerFont(TTFont('PoppinsMedium', os.path.join(settings.BASE_DIR, 'website_hr','static', 'resumebuilder', 'fonts', 'poppins-medium.ttf')))
registerFontFamily('Title', normal='FontAwesome', bold='PoppinsMedium')
registerFontFamily('Inconsolata', normal='Inconsolata', bold='InconsolataBold')
registerFontFamily('Poppins', normal='Poppins', bold='PoppinsBold', boldItalic='PoppinsBoldItalic')

styles = getSampleStyleSheet()


styles.add(ParagraphStyle(name='Content',
                    fontFamily='Poppins',
                    fontSize=10,
                    ))

styles.add(ParagraphStyle(name='SectionTitle', 
                          spaceBefore=1,
                          leading=20,
                          fontFamily ='Title', 
                          fontSize=15))



styles.add(ParagraphStyle(name='Normal_LEFT',
                          parent=styles['BodyText'],
                          fontName='Poppins',
                          wordWrap='LTR',
                          alignment=TA_LEFT,
                          fontSize=9,
                          leading=15,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=1,
                          spaceBefore=1,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))

styles.add(ParagraphStyle(name='Content_Text',
                          parent=styles['BodyText'],
                          fontName='Poppins',
                          wordWrap='LTR',
                          fontSize=9,
                          leading=13,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=12,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))
styles.add(ParagraphStyle(name='Content_HEAD',
                          fontName ='PoppinsMedium', 
                          fontSize=13))

def resume_builder(request):
    work_experience_formset = WorkExperienceFormSet(prefix='work-experience')
    education_formset = EducationFormSet(prefix='education')
    skills_formset = SkillsFormSet(prefix='skills')
    context = {
        'nbar': 'resumeBuilder',
        'work_experience_formset': work_experience_formset,
        'education_formset':education_formset,
        'skills_formset':skills_formset,
    }
    return render(request, 'resume_builder.html', context)


# Set the page height and width
HEIGHT = 10 * inch
WIDTH = 5 * inch

#Method to Generate Boilerplate
def generate_boilerplate(contact):
    def firstPage(canvas, doc):
        canvas.saveState()
        canvas.setFont('PoppinsMedium', 30)  # set the font for the name
        canvas.drawImage(contact['pfp'], .7 * inch,
            HEIGHT - (.3* inch), width=50, height=50)
        
        canvas.drawString(1.5 * inch,
            HEIGHT, contact['name']) # draw the name on top left page 1
        
        canvas.setFont("Helvetica", 15)
        canvas.drawString(1.5 * inch,
            HEIGHT - (.3 * inch), contact['position'])

        #new
        # canvas.setStrokeColor('#001682')
        # canvas.line(6.4 * inch, HEIGHT - (.85 * inch), 
        #      7.6 * inch, HEIGHT - (.85 * inch))



        # restore the state to what it was when saved
        canvas.restoreState()
    return firstPage

#Method to Generate Content
def create_resume(content, contacts, basic_info):
    buff = io.BytesIO()

    resume_pdf = SimpleDocTemplate(
        buff, 
        pagesize=letter, 
        rightMargin = .5 * inch, 
        leftMargin = .5 * inch,
        topMargin = 1.5*inch,
        bottomMargin = 1.5*inch,  
    )
    story = []

    tb1_w = 5*inch
    tb2_w = 2.5*inch

    data = [[content, contacts]]

    resume_dataTable = Table(
        data, 
        colWidths=[tb1_w,
                   tb2_w
                   ],
        hAlign='LEFT'
    )

    resume_dataTable.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONT', (0, 0), (-1, -1), 'Poppins'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), "LEFT"),
        ('VALIGN',(0,0),(-1, -1),'TOP')])
        )
    story.append(resume_dataTable)
    resume_pdf.build(
        story, 
        onFirstPage=generate_boilerplate(basic_info),
    )

    buff.seek(0)
    
    return FileResponse(buff, as_attachment=True, filename='aspire-resume.pdf')
    


def generate_resume(request):
    work_experience_formset = WorkExperienceFormSet(prefix='work-experience')
    education_formset = EducationFormSet(prefix='education')
    skills_formset = SkillsFormSet(prefix='skills')
    if request.method == 'POST':
        work_experience_formset = WorkExperienceFormSet(request.POST, prefix='work-experience')
        education_formset = EducationFormSet(request.POST, prefix='education')
        skills_formset = SkillsFormSet(request.POST, prefix='skills')
        #get all the data from form
        pfp = request.FILES.get('profile_pic')
        profile_pic=ImageReader(io.BytesIO(pfp.read())) #convert InMemoryUploadedFile to raw bytes
        position = request.POST.get('position')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone_number')
        profile_txt = request.POST.get('profile_body')

        experience_list = []
        education_list = []
        skills_list = []
        #work Experience
        if work_experience_formset.is_valid():
            print(work_experience_formset.forms)
            for item in work_experience_formset.forms:
                if item.has_changed():
                    # create a formatted string using the data
                    employment_title = item.cleaned_data['emp_position']
                    employment_startMonth = item.cleaned_data['emp_StartMonth']
                    employment_startYear = item.cleaned_data['emp_StartYear']
                    employment_endMonth = item.cleaned_data['emp_EndMonth']
                    employment_endYear = item.cleaned_data['emp_EndYear']
                    employment_desc = item.cleaned_data['emp_description']

                    formatted_string = ''.join([f'<b>{employment_title}</b><br/>',
                        f'<alignment=TA_RIGHT>{employment_startMonth} {employment_startYear} - {employment_endMonth} {employment_endYear}</alignment><br/>',
                        f'{employment_desc}<br/><br/>'])

                
                    
                    experience_list.append(formatted_string)
            

            print(education_list)


        
        #Education
        if education_formset.is_valid():
            
            for item in education_formset.forms:
                if item.has_changed():
                    
                    # create a formatted string using the data
                    school_name = item.cleaned_data['school_name']
                    school_location = item.cleaned_data['school_location']
                    degree = item.cleaned_data['degree']
                    field_of_study = item.cleaned_data['field_of_study']
                    startYear = item.cleaned_data['startYear']
                    endYear = item.cleaned_data['endYear']

                    formatted_string = '<br/>'.join([f'<b>{school_name}</b> {school_location}',
                        f'<b>{degree} </b>in {field_of_study}',
                        f'<b>{startYear} </b> - <b>{endYear} </b> <br/><br/>'])
                    
                    
                    
                    education_list.append(formatted_string)

            

        # SKills Formset
        if skills_formset.is_valid():
            
            for item in skills_formset:
                if item.has_changed():
                
                    # create a formatted string using the data
                    skiill_set = item.cleaned_data['skillset']
                    skills = item.cleaned_data['skills']

                    formatted_string = '<br/>'.join([
                        f'<b>{skiill_set}:</b>  {skills}<br/><br/>'
                        ])
                    
                    
                    
                    skills_list.append(formatted_string)

            
        
        #create canvas
        
        basic_info = {
            'pfp': profile_pic,
            'name': name,
            'position': position,
            
        }

        contact_info = [email, phone, address]


        data = {
        'profile': [f'{profile_txt}<br/><br/>'],
        'experience': [experience for experience in experience_list],
        'education': [education for education in education_list],
        'skills': [skill for skill in skills_list],
        
        }

    tblContact = [
        Paragraph('''<font name="FontAwesome" size="12">\uf05a&nbsp;</font><font name="PoppinsMedium" size="13">Details</font>''', styles['SectionTitle']),
        [Paragraph(x, styles['Normal_LEFT']) for x in contact_info],
    ]

    tblContent = [
        [Paragraph('''<font name="FontAwesome" size="12">\uf007&nbsp;</font><font name="PoppinsMedium" size="13">Profile</font>''', styles['SectionTitle'])],
        [[Paragraph(x, styles['Content']) for x in data['profile']]],
        [Paragraph('''<font name="FontAwesome" size="12">\uf0f2&nbsp;</font><font name="PoppinsMedium" size="13">Experience</font>''', styles['SectionTitle'])],
        [[Paragraph(x, styles['Content']) for x in data['experience']]],
        [Paragraph('''<font name="FontAwesome" size="12">\uf0e7&nbsp;</font><font name="PoppinsMedium" size="13">Skills</font>''', styles['SectionTitle'])],
        [[Paragraph(x, styles['Content']) for x in data['skills']]],
        [Paragraph('''<font name="FontAwesome" size="12">\uf19d&nbsp;</font><font name="PoppinsMedium" size="13">Education</font>''', styles['SectionTitle'])],
        [[Paragraph(x, styles['Content']) for x in data['education']]],
        
        ]

    
    return create_resume(tblContent, tblContact, basic_info)
