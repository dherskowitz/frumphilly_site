from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ads.models import Ad, ad_prices
from pages.models import Contact, SUBJECT_CHOICES, ReportPost, REPORT_REASON_CHOICES
from payments.models import Payment


@login_required
def admin_review_ad(request, uuid):
    ad = Ad.objects.get(redirect_uuid=uuid)
    payments = Payment.objects.filter(ad_uuid=ad.redirect_uuid)
    price_info = ad_prices[f"{ad.contract_length}"]

    context = {
        "ad": ad,
        "payments": payments,
        "price_info": price_info
    }
    return render(request, "admin/ads/single.html", context)


@login_required
def admin_all_ads(request):
    ads_obj = Ad.objects.all().order_by("-created_at")

    filtered_type = request.GET.getlist('type', None)
    if filtered_type:
        ads_obj = ads_obj.filter(type__in=filtered_type)
    filtered_status = request.GET.getlist('status', None)
    if filtered_status:
        ads_obj = ads_obj.filter(status__in=filtered_status)
    filtered_term = request.GET.getlist('term', None)
    if filtered_term:
        ads_obj = ads_obj.filter(contract_length__in=filtered_term)

    # set pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(ads_obj, 15)
    try:
        ads_obj = paginator.page(page)
    except PageNotAnInteger:
        ads_obj = paginator.page(1)
    except EmptyPage:
        ads_obj = paginator.page(paginator.num_pages)

    context = {
        "ads": ads_obj,
        "filtered_type": filtered_type,
        "filtered_status": filtered_status,
        "filtered_term": filtered_term,
        "status_choices": Ad.STATUS_CHOICES,
        "type_choices": Ad.TYPE_CHOICES,
        "term_choices": Ad.TERM_CHOICES
    }
    return render(request, "admin/ads/list.html", context)


@login_required
def contact_submissions(request):
    if not request.user.has_perm('pages.change_contact') and not request.user.has_perm('pages.delete_contact'):
        return render(request, "403.html")

    # Get all contacts sorted by create date
    contacts = Contact.objects.all().order_by("-created_at")

    filtered_name = request.GET.get('name', None)
    if filtered_name:
        contacts = contacts.filter(name__icontains=filtered_name)
    filtered_subject = request.GET.getlist('subject', None)
    if filtered_subject:
        contacts = contacts.filter(subject__in=filtered_subject)
    filtered_status = request.GET.getlist('status', None)
    if filtered_status:
        contacts = contacts.filter(status__in=filtered_status)

    # set pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(contacts, 15)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    # add data to context and return
    context = {
        "contacts": contacts,
        "subjects": SUBJECT_CHOICES[1::],
        "statuses": Contact.STATUS_CHOICES,
        "filtered_name": filtered_name,
        "filtered_subject": filtered_subject,
        "filtered_status": filtered_status,
    }

    return render(request, "admin/contact_submissions/list.html", context)


@login_required
def contact_message(request, contact_id):
    if not request.user.has_perm('pages.change_contact') and not request.user.has_perm('pages.delete_contact'):
        return render(request, "403.html")
    message = get_object_or_404(Contact, id=contact_id)
    context = {
        "contact": message,
    }
    return render(request, "admin/contact_submissions/single.html", context)


@login_required
def toggle_status(request):
    if not request.user.has_perm('pages.change_contact') and not request.user.has_perm('pages.delete_contact'):
        return render(request, "403.html")
    if request.htmx:
        message_id = request.GET.get('message_id')
        new_status = request.GET.get('message_status')

        message = Contact.objects.get(id=message_id)
        context = {
            "contact": message
        }

        message.status = new_status
        message.save()
        return render(request, "admin/contact_submissions/_contact_status.html", context)


@login_required
def delete_message(request, message_id):
    if not request.user.has_perm('pages.change_contact') and not request.user.has_perm('pages.delete_contact'):
        return render(request, "403.html")

    if request.method == "POST":
        message = get_object_or_404(Contact, id=message_id)
        message.delete()
        success_url = reverse("contact_submissions")
        if request.htmx:
            return render(request, "admin/contact_submissions/_message_deleted.html")
        return redirect(success_url)


@login_required
def reported_posts(request):
    if not request.user.has_perm('pages.change_reportpost') and not request.user.has_perm('pages.delete_reportpost'):
        return render(request, "403.html")

    # Get all contacts sorted by create date
    obj = ReportPost.objects.all().order_by("-created_at")
    post_types = obj.values_list('post_type').distinct()

    filtered_type = request.GET.getlist('post_type', None)
    if filtered_type:
        obj = obj.filter(post_type__in=filtered_type)
    filtered_reason = request.GET.getlist('report_reason', None)
    if filtered_reason:
        obj = obj.filter(report_reason__in=filtered_reason)

    # set pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(obj, 15)
    try:
        obj = paginator.page(page)
    except PageNotAnInteger:
        obj = paginator.page(1)
    except EmptyPage:
        obj = paginator.page(paginator.num_pages)

    # add data to context and return
    context = {
        "posts": obj,
        "post_types": post_types,
        "report_reasons": REPORT_REASON_CHOICES[1::],
        "filtered_type": filtered_type,
        "filtered_reason": filtered_reason,
    }

    return render(request, "admin/reported_posts/list.html", context)


@login_required
def reported_post(request, post_id):
    if not request.user.has_perm('pages.change_reportpost') and not request.user.has_perm('pages.delete_reportpost'):
        return render(request, "403.html")
    post = get_object_or_404(ReportPost, id=post_id)
    context = {
        "post": post,
    }
    return render(request, "admin/reported_posts/single.html", context)
