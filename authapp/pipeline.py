from django.http import HttpResponse
from django.shortcuts import redirect
from website_hr.forms import ApplyLinkedinForm
from social_core.pipeline.partial import partial

@partial
def capture_user_data(request, backend, details, *args, **kwargs,):
    if backend.name == 'linkedin-oauth2':
        data = {
            'id': kwargs['response']['id'],
            'email': kwargs['response']['emailAddress'],
            'first_name': kwargs['response']['firstName']['localized']['en_US'],
            'last_name': kwargs['response']['lastName']['localized']['en_US'],
            # 'profile_url': f"http://www.linkedin.com/in/{kwargs['response']['id']}",
        }
        
        
         # Store the form in the session for use in the next pipeline step
        request.session['apply_linkedin_form'] = data
        job = request.session['job_url']
        print(job)
        print({f"{data} yes"})
        return redirect('jobDetails', job_id=job)