from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from .models import CustomUser
from django.core.paginator import Paginator

@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        #users = CustomUser.objects.all()
        #data = {'results': list(users.values('id','user__username', 'first_name', 'last_name', 'email'))}
        #return JsonResponse(data)
        # Set the number of users to display per page
        per_page = 5
        
        # Get the page number from the request's GET parameters
        page_number = request.GET.get('page', 1)
        
        # Get the users, ordered by id
        users = CustomUser.objects.order_by('id')
        
        # Paginate the users
        paginator = Paginator(users, per_page)
        page = paginator.get_page(page_number)
        
        # Get the user data for the current page
        data = {
            'results': list(page.object_list.values('id','user__username', 'first_name', 'last_name', 'email')),
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'page_number': page_number,
            'num_pages': paginator.num_pages,
        }
        
        return JsonResponse(data)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(
            username=data['username'], 
            email=data['email'], 
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        CustomUser.objects.create(
            user=user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        return JsonResponse({'message': 'User created successfully.'}, status=201)

@csrf_exempt
def user_detail(request, pk):
    user = CustomUser.objects.filter(pk=pk).first()
    if not user:
        print("not siya")
        return JsonResponse({'message': 'User not found'}, status=404)
    #try:
        user = get_object_or_404(CustomUser, pk=pk)
    #except Http404:
    #    return JsonResponse({'message': 'User not found'}, status=404)
    
    if request.method == 'GET':
        data = {
            'username': user.user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        user.user.username = data['username']
        user.user.email = data['email']
        user.user.first_name = data['first_name']
        user.user.last_name = data['last_name']
        user.user.save()
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.save()
        return JsonResponse({'message': 'User updated successfully.'})
    
    elif request.method == 'DELETE':
        user.user.delete()
        return JsonResponse({'message': 'User deleted successfully.'})
