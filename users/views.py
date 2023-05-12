from django.shortcuts import render,redirect
from .models import Profile,Message
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm,ProfileForm,SkillForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Skill
from django.db.models import Q
from .utils import searchProfiles,paginateProfiles
# Create your views here.



def LoginPage(request):
    page="login"

    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username) # check if user is there
        except:
            messages.error(request,'Username does not exist')
        user = authenticate(username=username,password=password)

        if user is not None:
           login(request,user) # create a session for user
           if 'next' in request.GET:
            return redirect(request.GET['next'])
           else:
               return redirect('profiles')
               
        else:
            messages.error(request,'Username or password is incorrect') 
    context = {"page":page}
    return render(request, 'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.success(request,"User Logged out successfully!!")
    return redirect('login')



def registerUser(request):
    page="register"
    form =  CustomUserCreationForm()# wil create the form
    if request.method=="POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #create user object but not commit as we need to do some processing
            user.username = user.username.lower()
            user.save()
            messages.success(request,"User account created!!")
            login(request,user)
            return redirect('profiles')
        else:
            messages.success(request,"Error in creating user!!")
    context={"page":page,"form":form}

    return render(request, 'users/login_register.html',context)

def Profiles(request):

    profiles,search_query = searchProfiles(request)
    custom_range,profiles = paginateProfiles(request,profiles,3)

    context = {"profiles":profiles,'search_query':search_query,"custom_range":custom_range}
    return render(request,'users/profiles.html',context)


def UserProfile(request,pk):
    profile = Profile.objects.get(profile_uuid = pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="") 
    context = {"profile":profile,"topSkills":topSkills,"otherSkills":otherSkills}
    return render(request,'users/user-profile.html',context)



@login_required(login_url='login')
def UserAccount(request):
    profile = request.user.profile 
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile":profile,"skills":skills,"projects":projects}


    return render(request,'users/account.html',context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm()
    if request.method=="POST":
        form = ProfileForm(request.POST,request.FILE,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {"form":form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile 
    form = SkillForm()
    if request.method=="POST":

        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)

            skill.owner = profile 

            skill.save()

            messages.success(request,"Skill Added Successfully")
            return redirect('user-account')
    context = {'form':form}
    return render(request,'users/skill_form.html',context)



@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(skills_uuid = pk)
    form = SkillForm(instance = skill) # get prefilled info

    if request.method == 'POST':
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill Edited Successfully!!")

            return redirect('user-account')
    context = {'form':form}
    return render(request,'users/skill_form.html',context)


@login_required(login_url='login')
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(skills_uuid=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request,"Skill deleted Successfully!!")
        return redirect('user-account')

    context = {"object":skill}
    return render(request,"delete_template.html",context)


@login_required(login_url='login')
def inbox(request):
    user = request.user
    msgs = Message.objects.filter(recipient__user  = user)

    print(msgs)    
    context =  {}
    return render(request,'users/inbox.html',context)