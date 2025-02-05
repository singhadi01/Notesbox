from django.shortcuts import render, redirect
from .models import Video, Subject
from .apps import VideosConfig
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai
from django.conf import settings
import random
import string

@login_required(login_url="/login/")
def home(request):
    if request.method == "POST":
        data = request.POST
        video_title = data.get('videoTitle')

        if data.get('subject') != "Other":
            subject_name = data.get('subject')
        else:
            subject_name = data.get('otherSubject')

        user = request.user
        subject, created = Subject.objects.get_or_create(name=subject_name,user=user)

        user = request.user  

        Video.objects.create(
            user=user,
            subject=subject, 
            title=video_title,
            link=data.get('link')
        )
        return redirect("/")
    subjects = Subject.objects.filter(video__user=request.user).distinct()  # Fetch all subjects with their videos
    context = {'subjects': subjects}
    return render(request, "index.html", context)

@login_required(login_url="/login/")
def delete_subject(request, id):
    try:
        subject = Subject.objects.get(id=id, user=request.user) 
        Video.objects.filter(subject=subject, user=request.user).delete()
        # Now delete the subject itself
        subject.delete()
        messages.success(request, "Subject and associated videos deleted successfully!")
        
    except Subject.DoesNotExist:
        messages.error(request, "You cannot delete this subject!")
    
    return redirect('/')

@login_required(login_url="/login/")
def delete_video(request, video_title):
    video_title = video_title.replace('%20', ' ')
    videos = Video.objects.filter(title=video_title, user=request.user)
    
    if videos.exists():
        video_to_delete = videos.first()
        subject = video_to_delete.subject 
        video_to_delete.delete()
        if not Video.objects.filter(subject=subject).exists():
            subject.delete()
        messages.success(request, "Video deleted successfully!")
    else:
        messages.error(request, "Video not found or you don't have permission to delete it.")
    
    return redirect('/')


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('/login/')

def login_page(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password =request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username")
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        
        if user is None:
            messages.info(request, "Invalid Credential")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/')
            
            
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password =request.POST.get('password')
        print(f"First Name: {first_name}, Last Name: {last_name}, Username: {username}, Password: {password}")
        
        user=User.objects.filter(username=username)
        if user.exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account Created")
        return redirect('/login/')
    return render(request,'register.html')

@login_required
def copy_subject_by_code(request):
    if request.method == 'POST':
        code = request.POST.get('sharedcode')

        try:
            # Look up the subject by the provided code
            subject = Subject.objects.get(code=code)
            if Subject.objects.filter(name=f"{subject.name} by {subject.user.username} for {request.user.username}", user=request.user).exists():
                    messages.error(request, "A subject with this name already exists!")
                    return redirect('/')
            # Check if the user is not the owner of the subject
            if subject.user != request.user:
                print(f"User is not the owner, proceeding with copying the subject.")
                while True:
                    unique_string = ''.join(random.choices(string.digits, k=4))
                    if not Subject.objects.filter(code__icontains=unique_string).exists():
                        break
                copied_subject = Subject(
                    name=f"{subject.name} by {subject.user.username} for {request.user.username}",
                    user=request.user,
                    code=f"{subject.code}({unique_string})"
                )
                copied_subject.save()  
                print(f"Copied subject saved with ID: {copied_subject.id}")
                
                for video in Video.objects.filter(subject=subject):
                    print(f"Copying video: {video.title} for subject {copied_subject.name}")
                    new_video = Video(
                        user=request.user,
                        subject=copied_subject,
                        title=video.title,
                        link=video.link,
                        embed_link=video.embed_link
                    )
                    new_video.save()  
                    print(f"Video saved: {new_video.title}")
                messages.success(request, "Subject and videos copied successfully!")
                return redirect('/') 
            else:
                messages.error(request, "You cannot copy your own subject!")
                return redirect('/')
        except Subject.DoesNotExist:
            messages.error(request, "Invalid subject code!")
            return redirect('/')

    return render(request, 'index.html')
def get_gemini_response(input_text):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[] 
    )

    response = chat_session.send_message(input_text)
    return response.text

def chat_view(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            user_input = request.POST.get("input_text")
            if not user_input:
                return JsonResponse({'message': 'No input provided'}, status=400)
            print(f"User input: {user_input}")

            response_text = get_gemini_response(user_input)
            print(f"Gemini response: {response_text}")

            return JsonResponse({'message': response_text})

        except Exception as e:
            print(f"Error processing the request: {e}")
            return JsonResponse({'message': 'An error occurred'}, status=500)

    return render(request, "index.html")