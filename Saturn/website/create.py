from section.models import(
        Section,
        Post,
        List,
	 About,
         File
        )
from website.models import(
        PageLinks,
        Website
        )

import json

class Create(object):

    ABOUT_COURSE = "About"
    COURSE_SYLLABUS = "Syllabus"
    INSTRUCTORS = "Instructors"
    GRADES = "Grades"
    TAS = "TA"
    EXAMS = "Exams"


    @staticmethod
    def aboutSection(user, template, title, description,image=None):
        valid = False
        section = About.objects.create(user=user,template=template)
        if description:
            valid = True
            section.title = title
            section.content = description
        if image:
            image_file  = File.objects.filter(content=image)
            if image_file.exists():
                valid = True
                section.image = image_file[0]
        if valid:
            section.save()
            print "image saved"
        else:
            section.delete()
            

    @staticmethod
    def listSection(user, template, title, string):
        valid = False
        section = List.objects.create(user=user,template=template)
        if title:
            valid = True
            section.title = title
        if Create.arrayExists(string):
            valid = True
            section.items = string
        if valid:
            section.save()
            return section
        else:
            section.delete()
            return False
    
    @staticmethod
    def syllabusSection(user, template, string):
        if string:
            section = Post.objects.create(user=user, template=template)
            section.content = string
            section.title = Create.COURSE_SYLLABUS 
            section.save()
            return section
        else:
            return False

    @staticmethod
    def pageLinks(user, template,currentWebsite, string):
        if Create.arrayExists(string):
            links = json.loads( string )
            for link in links:
                w = Website.objects.filter(domain=link,user=user)
                if w.exists():
                    pl = PageLinks.objects.create(fromSite=currentWebsite,toSite=w[0])
                    pl.save()

    '''
    checks whether or not an array of values exist inside
    of the string
    '''
    @staticmethod
    def arrayExists(string):
        variable = ''
        try:
            variable = json.loads( string )
        except ValueError, e:
            return False
        if len(variable) == 1 and variable[0] == '':
            return False 
        elif len(variable):
            return True
        else:
            return False

