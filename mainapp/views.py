from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    return render(request,"backend/index.html")

def adduser(request):
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
        return render(request, 'app/add-job.html')  # Replace with your success template name
    else:
        return render(request, 'app/add-job.html')
    # Handle GET requests (render the form template)
def jobs (request):
    return render(request, 'backend/ui-cards.html')