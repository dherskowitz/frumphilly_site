from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from forum.models import ForumCategory, ForumThread, ForumPost


def forum(request):
    categories = ForumCategory.objects.all() #.annotate(threads_count=Count('threads'))
    context = {
        "categories": categories
    }
    return render(request, "forum/index.html", context)


def forum_category(request, category):
    # TODO paginate threads
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
    # TODO paginate posts
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

