from django.shortcuts import render
from .models import Education,WorkExperience,Skill
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.
from .models import AppliedJob,JobOpening
from django.contrib.auth.models import User

def index(request):
    return render(request,"test.html")

def home(request):
    return render(request,"profile/profile.html")

def applicants(request):

    company_names = JobOpening.objects.values_list('company_name', flat=True)
    if request.POST:
            selected_company = request.POST.get('company_name')
            company = JobOpening.objects.filter(company_name=selected_company).first()
            print(selected_company)
            users_applied = company.appliedjob_set.all()
            print(users_applied)
            user = request.user
            applied_jobs = AppliedJob.objects.filter(user=user)

            return render(request, "hr/applicants.html", {"company":company_names,"appliedUsers":users_applied})
    return render(request, "hr/applicants.html", {"company":company_names})


def applyjob(request):
    user = request.user
    company_names = JobOpening.objects.values_list('company_name', flat=True)
    selected_company = request.POST.get('company_name')
    # request.session['selected_company'] = selected_company

    if request.method == 'POST' and request.FILES['pdf_files']:
        uploaded_file = request.FILES['pdf_files']
        selectedCompany = JobOpening.objects.get(company_name=selected_company)

        file_instance = AppliedJob(user=user,file=uploaded_file,company=selectedCompany)
        file_instance.save()
        return render(request, "user/apply.html")
    return render(request,"user/apply.html",{"jobs":company_names})




def addworkexp(request):
    company_names = JobOpening.objects.values_list('company_name', flat=True)

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
        return render(request,'user/apply.html',{"jobs":company_names})
    return render(request,'user/apply.html',{"jobs":company_names})

# @login_required
def addeducation(request):
    company_names = JobOpening.objects.values_list('company_name', flat=True)

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
        return render(request,'user/apply.html',{"jobs":company_names})
    return render(request,'user/apply.html',{"jobs":company_names})

# @login_required
def addskills(request):

    company_names = JobOpening.objects.values_list('company_name', flat=True)

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
        return render(request,'user/apply.html',{"jobs":company_names})
    return render(request,'user/apply.html',{"jobs":company_names})

from .models import *

def addJob(request):
    if request.method == 'POST':
        company_name = request.POST.get('cname')
        job_title = request.POST.get('jname')
        job_description = request.POST.get('jd')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        deadline_date = request.POST.get('dedline')

        # Print the form data to the console
        print(f"formData: {{ company_name: '{company_name}', job_title: '{job_title}', job_description: '{job_description}', salary: '{salary}', location: '{location}', deadline_date: '{deadline_date}' }}")
        
        
        job_opening = JobOpening(
            company_name=company_name,
            job_title=job_title,
            job_description=job_description,
            salary=salary,
            location=location,
            deadline_date=deadline_date
        )
        job_opening.save()

        # You can optionally process the form data here (e.g., save it to a database)

        # Return a success response (optional)
        return render(request, 'hr/addJob.html')  # Replace with your success template name
    else:
        return render(request, 'hr/addJob.html')
    

def listjob(request):
    job_openings = JobOpening.objects.all()  # Fetch all job openings from the database
    context = {'job_openings': job_openings}
    return render(request, 'hr/listjob.html', context)



def profile(request):
    user = request.user
    education = Education.objects.filter(user=user)
    workexp = WorkExperience.objects.filter(user=user)
    skill_info = Skill.objects.filter(user=user)
    print(education)
    print(workexp)
    print(skill_info)
    params = {
        'education':education,
        'workexp':workexp,
        'skill':skill_info
    } 
    return render(request,'profile/profile.html', params)