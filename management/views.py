from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ads.models import Ad, ad_prices
from pages.models import Contact, SUBJECT_CHOICES
from payments.models import Payment


@login_required
def admin_review_ads(request):
    ads = Ad.objects.filter(status='review').order_by("-created_at")

    context = {
        "ads": ads,
    }
    return render(request, "admin/ad_review_all.html", context)


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
    return render(request, "admin/ad_review_single.html", context)


@login_required
def admin_all_ads(request):
    context = {
        "ads": Ad.objects.all().order_by("-created_at")
    }
    return render(request, "admin/ads_all.html", context)


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
    message = Contact.objects.get(id=contact_id)
    context = {
        "message": message,
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
        return render(request, "admin/contact_submissions/_contact_row.html", context)


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