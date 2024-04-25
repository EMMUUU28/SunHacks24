from django.shortcuts import render
from .models import Education,WorkExperience,Skill
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.
from .models import AppliedJob

def index(request):
    return render(request,"test.html")

def applyjob(request):
    user = request.user
    if request.method == 'POST' and request.FILES['pdf_files']:
        uploaded_file = request.FILES['pdf_files']
        file_instance = AppliedJob(user=user,file=uploaded_file)
        file_instance.save()
        return render(request, "user/apply.html")
    return render(request,"user/apply.html")


def addworkexp(request):
    if request.method == 'POST':
        
        company = request.POST.get('company')
        position = request.POST.get('position')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        brief = request.POST.get('brief')
        
        # Print form data
        print(f"Company: {company}")
        print(f"Position: {position}")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        print(f"Brief: {brief}")
        user = request.user

        WorkExperience.objects.create(
            user=user,
            company=company,
            position=position,
            start_date=start_date,
            end_date=end_date,
            description=brief,
        )
        
        # Do something with the form data, such as saving to a database
        return render(request,'user/apply.html')
    return render(request,'user/apply.html')

# @login_required
def addeducation(request):
    if request.method == 'POST':
        institution = request.POST.get('institution')
        degree = request.POST.get('degree')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        user = request.user
       
        # Print form data
        print(f"Institution: {institution}")
        print(f"Degree: {degree}")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")

        Education.objects.create(
            user=user,
            institution=institution,
            degree=degree,
            start_date=start_date,
            end_date=end_date,
        )
        
        # Do something with the form data, such as saving to a database
        return render(request,'user/apply.html')
    return render(request,'user/apply.html')

# @login_required
def addskills(request):
    if request.method == 'POST':
        user = request.user

        skills = request.POST.get('skills')
        
        skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]  # Split skills by comma and remove any empty or whitespace-only skills
        
        # Print individual skills
        for skill in skills_list:
            print(f"Skill: {skill}")

        for skill_name in skills_list:
                Skill.objects.create(user=user, skill_name=skill_name)

        
        # Do something with the form data, such as saving to a database
        return render(request,'user/apply.html')
    return render(request,'user/apply.html')
