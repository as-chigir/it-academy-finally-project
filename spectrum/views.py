from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from . import constants
from . import forms
from . import models


def all_ads_(request):
    all_ads = models.Ads.objects.all()
    return render(request, "ads/all_ads.html",
                  {"ads": all_ads})


def all_news_(request):
    all_news = models.News.objects.all()
    return render(request, "news/all_news.html",
                  {"news": all_news})


def detailed_ads_(request, year, month, day, slug):
    detailed_ads = get_object_or_404(models.Ads,
                                     publish__year=year,
                                     publish__month=month,
                                     publish__day=day,
                                     slug=slug)
    return render(request, "ads/detailed_ads.html",
                  {"ad": detailed_ads})


def detailed_news_(request, year, month, day, slug):
    detailed_news = get_object_or_404(models.Ads,
                                      publish__year=year,
                                      publish__month=month,
                                      publish__day=day,
                                      slug=slug)
    return render(request, "news/detailed_news.html",
                  {"new": detailed_news})


def share_ads(request, ad_id):  # отправить комментарии
    ad = get_object_or_404(models.Ads, id=ad_id)
    sent = False
    if request.method == "POST":
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ad_uri = request.build_absolute_uri(
                ad.get_absolute_url(),
            )
            subject = constants.SHARE_EMAIL_SUBJECT.format(
                cd['name'],
                ad.title,
            )
            body = constants.SHARE_EMAIL_BODY.format(
                title=ad.title,
                uri=ad_uri,
                comment=cd['comment'],
            )

            send_mail(subject, body, 'admin@my.com', [cd['to_email'], ])
            sent = True
    else:
        form = forms.EmailMaterialForm()

    return render(request,
                  'ads/share_ads.html',
                  {'ad': ad, 'form': form, 'sent': sent})
