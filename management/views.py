from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from ads.models import Ad, ad_prices
from pages.models import Contact
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
    if not request.user.has_perm('pages.can_change_contact') and not request.user.has_perm('pages.can_delete_contact'):
        return render(request, "403.html")

    contacts = Contact.objects.all().order_by("-created_at")
    page = request.GET.get("page", 1)
    paginator = Paginator(contacts, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        "contacts": contacts,
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
    if not request.user.has_perm('pages.can_change_contact') and not request.user.has_perm('pages.can_delete_contact'):
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
