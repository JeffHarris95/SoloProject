from unicodedata import category
from django.shortcuts import render, HttpResponse, redirect
from .models import User, Article, Post
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if request.session.is_empty():
        return render(request, 'index.html')
    else:
        context = {
            "user" : User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'index.html', context)

def loginreg(request):
    return render(request, 'loginreg.html')

def newpostpage(request):
    return render(request, 'newpost.html')

def purchase(request):
    return render(request, 'purchase.html')

def news(request):
    if request.session.is_empty():
        context = {
            "all_articles" : Article.objects.all()
        }
        return render(request, 'news.html', context)
    else:
        context = {
            "user" : User.objects.get(id=request.session['user_id']),
            "all_articles" : Article.objects.all()
        }
        return render(request, 'news.html', context)

def forum(request):
    if request.session.is_empty():
        context = {
            "all_posts" : Post.objects.all()
        }
        return render(request, 'forum.html', context)
    else:
        context = {
            "user" : User.objects.get(id=request.session['user_id']),
            "all_posts" : Post.objects.all()
        }
        return render(request, 'forum.html', context)

def shop(request):
    if request.session.is_empty():
        return render(request, 'shop.html')
    else:
        context = {
            "user" : User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'shop.html', context)

def register(request):
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        return redirect('/loginreg')
    
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email_address=request.POST['email'],
            password= pw_hash
            )
        request.session['user_id'] = new_user.id
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    else:
        logged_user = User.objects.get(email_address=request.POST['email'])
        request.session['user_id'] = logged_user.id
        context = {
            "user" : User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'index.html', context)

def newarticlepage(request):
    return render(request, 'newarticle.html')

def newarticle(request):
    new_article = Article.objects.create(
        title=request.POST['title'],
        description=request.POST['description'],
    )
    return redirect('/news')

def likearticle(request, article_id):
    article = Article.objects.get(id=article_id)
    logged_user = User.objects.get(id=request.session['user_id'])
    logged_user.liked_books.add(article)
    return redirect('/news')

def addpost(request):
    errors = Post.objects.post_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/createpost')
    
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        new_post = Post.objects.create(
            title=request.POST['title'],
            category=request.POST['category'],
            description=request.POST['description'],
            created_by=logged_user,
            )
    return redirect('/forum')

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "post" : Post.objects.get(id=post_id),
        "all_users" : User.objects.all()
    }
    return render(request, 'post.html', context)

def editpost(request, post_id):
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "post" : Post.objects.get(id=post_id),
    }
    return render(request, 'editpost.html', context)

def update(request, post_id):
    errors = Post.objects.post_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/editpost/'+ str(post_id))
    
    else:

        post_update = Post.objects.get(id=post_id)

        post_update.title=request.POST['title']
        post_update.category=request.POST['category']
        post_update.description=request.POST['description']

        post_update.save()

        return redirect('/forum')

def delete(request, post_id):
    delete_post = Post.objects.get(id=post_id)
    delete_post.delete()
    return redirect('/forum')