from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from forum.forms import ThreadCreateForm, PostCreateForm
from forum.models import ForumCategory, ForumThread, ForumPost


def forum(request):
    categories = ForumCategory.objects.all() #.annotate(threads_count=Count('threads'))
    context = {
        "categories": categories
    }
    return render(request, "forum/index.html", context)


def forum_category(request, category):
    threads = ForumThread.objects.filter(category__slug=category).all()
    c = ForumCategory.objects.get(slug=category)

    page = request.GET.get("page", 1)
    paginator = Paginator(threads, 10)
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.page(paginator.num_pages)

    context = {
        "category": c,
        "threads": threads
    }
    return render(request, "forum/threads.html", context)


def forum_thread(request, category, thread):
    t = ForumThread.objects.get(slug=thread)
    c = ForumCategory.objects.get(slug=category)
    posts = ForumPost.objects.filter(thread=t.id).order_by("created_at").all()

    page = request.GET.get("page", 1)
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "category": c,
        "thread": t,
        "posts": posts
    }
    return render(request, "forum/posts.html", context)


def forum_thread_create(request, category):
    c = ForumCategory.objects.get(slug=category)
    form = ThreadCreateForm()
    context = {
        "category": c,
        "form": form
    }

    if request.method == "POST":
        form = ThreadCreateForm(request.POST, request.FILES)
        context["form"] = form

        if form.is_valid():
            thread = form.save(commit=False)
            thread.category = c
            thread.owner = request.user
            thread.save()
            form.save_m2m()
            messages.success(request, "Thread created successfully!")
            return redirect(f"/forum/{c.slug}/")
    return render(request, "forum/thread_create.html", context)


def forum_post_create(request, category, thread):
    t = ForumThread.objects.get(slug=thread)
    c = ForumCategory.objects.get(slug=category)
    form = PostCreateForm()
    context = {
        "category": c,
        "thread": t,
        "form": form
    }

    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        context["form"] = form

        if form.is_valid():
            post = form.save(commit=False)
            post.thread = t
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Post added successfully!")
            return redirect(f"/forum/{c.slug}/{t.slug}")
    return render(request, "forum/post_create.html", context)


def forum_user_posts(request, user):
    posts = ForumPost.objects.filter(author__email=user).order_by("-created_at")
    context = {
        "posts": posts,
        "user": user,
        "posts_count": posts.count()
    }
    return render(request, "forum/user_posts.html", context)
