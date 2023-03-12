import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from userapi.models import CustomUser
from users.models import AjaxLog
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def ajax_view(request):
    if request.method == 'POST':
        # Log the request data
        ajax_log = AjaxLog(
            request_url=request.path,
            request_data=request.body,
            request_method=request.method,
        )

        # Process the request
        data = {'message': 'Hello, world!'}

        # Log the response data
        ajax_log.response_status = 200
        ajax_log.response_data = json.dumps(data)
        ajax_log.save()

        return JsonResponse(data)
def ajax_log_view(request):
    logs = AjaxLog.objects.all()
    return render(request, 'ajax_log.html', {'logs': logs})

def render_list(request):
    return render(request, 'home_page.html')

