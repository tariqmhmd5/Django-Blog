from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras


def blogHome(request):
    
    allpost = Post.objects.all().order_by('-timestamp')
    context ={
        'allpost': allpost
    }
    return(render(request,'blog/blogHome.html',context))

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comment = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict={}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)

    print(repDict)

    context = {
        'post': post,
        'comments': comment,
        'repDict': repDict,
    }
    return(render(request,'blog/blogPost.html', context))


def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno=="":
            com = BlogComment(comment=comment,post=post,user=user)
            com.save()
            messages.success(request,"Comment is posted")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            com = BlogComment(comment=comment,post=post,user=user,parent=parent)
            com.save()
            messages.success(request,"Reply is posted")
        
    return(redirect(f'/blog/{post.slug}'))
    