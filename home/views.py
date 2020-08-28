# pylint: disable=unused-variable
# pylint: enable=too-many-lines
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

def home(request):
    if request.method=='POST':
        title = request.POST['title']
        Bcontent = request.POST['Bcontent']
        author = request.user
        slug = slugify(title)

        blog = Post(title=title,author=author,slug=slug,content=Bcontent)
        blog.save()
        messages.success(request,"Your Blog is Posted sucessfully!")
    else:
        print('nahi chala')
    

    return(render(request,'home/home.html'))

def about(request):
    return(render(request,'home/about.html'))

def contact(request):
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        email = request.POST['email']
        content = request.POST['content']

        contact = Contact(fname=fname,lname=lname,email=email,phone=phone,content=content)
        contact.save()
        messages.success(request,"Message sent sucessfully!")

    return(render(request,'home/contact.html'))

def search(request):
    query = request.POST['query']
    if len(query)>78:
        allpost= Post.objects.none()
    else:
        alltitle = Post.objects.filter(title__icontains=query)
        allcontent = Post.objects.filter(content__icontains=query)
        allpost = alltitle.union(allcontent)
    
    context = {
            'allpost': allpost,
            'query': query
        }

    if allpost.count() == 0:
        messages.warning(request,"No Search results found please refine your query")
    
    return(render(request,'home/search.html',context))

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        email = request.POST['email']
        password = request.POST['password']

        myuser =User.objects.create_user(username,email,password)
        name=fname.split(" ")
        myuser.first_name = name[0]
        myuser.last_name = name[-1]
        myuser.save()
        messages.success(request,"Your Icoder Account is created sucessfully")
        return(redirect('home'))
    else:
        return(HttpResponse('404 Not Found'))
    
def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        loginuser = authenticate(username= loginusername,password= loginpass)

        if loginuser is not None:
            login(request,loginuser)
            messages.success(request, "Sucessfully Logged In")
            return(redirect('home'))
        else:
            messages.error(request, "Invalid username or password")
            return(redirect('home'))
            
    return(HttpResponse("404 Not Found"))

def handleLogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request,"Logged out Sucessfully")
        return(redirect('home'))



