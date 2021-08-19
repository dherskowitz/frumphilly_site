from django.shortcuts import render

from forum.models import ForumCategory, ForumThread, ForumPost


def forum(request):
    categories = ForumCategory.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "forum/index.html", context)


def forum_category(request, category):
    # TODO paginate threads
    threads = ForumThread.objects.filter(category__slug=category).all()
    context = {
        "threads": threads
    }
    return render(request, "forum/threads.html", context)


def forum_thread(request, category, thread):
    # TODO paginate posts
    t = ForumThread.objects.get(slug=thread)
    c = ForumCategory.objects.get(slug=category)
    posts = ForumPost.objects.filter(thread=t.id).all()
    context = {
        "category": c.title,
        "thread": t.title,
        "posts": posts
    }
    return render(request, "forum/posts.html", context)

