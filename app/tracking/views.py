from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import Garment


@login_required
def waiting_dryroom_page(request):
    garments = Garment.objects.filter(pqc_good__gt=0, dryroom_ci=0).order_by("-pqc_good_time")

    buyer = request.GET.get("buyer")
    style = request.GET.get("style")
    line = request.GET.get("line")
    wo = request.GET.get("wo")

    if buyer:
        garments = garments.filter(buyer__icontains=buyer)
    if style:
        garments = garments.filter(style__icontains=style)
    if line:
        garments = garments.filter(line__icontains=line)
    if wo:
        garments = garments.filter(wo__icontains=wo)

    context = {"garments": garments}
    return render(request, "tracking/waiting_dryroom.html", context)


@login_required
def waiting_folding_page(request):
    garments = Garment.objects.filter(dryroom_co__gt=0, folding_ci=0).order_by("-dryroom_co_time")

    rfid_garment = request.GET.get("rfid_garment")
    buyer = request.GET.get("buyer")
    style = request.GET.get("style")
    wo = request.GET.get("wo")
    color = request.GET.get("color")
    size = request.GET.get("size")
    line = request.GET.get("line")

    if rfid_garment:
        garments = garments.filter(rfid_garment=rfid_garment)
    if buyer:
        garments = garments.filter(buyer__icontains=buyer)
    if style:
        garments = garments.filter(style__icontains=style)
    if wo:
        garments = garments.filter(wo__icontains=wo)
    if color:
        garments = garments.filter(color__icontains=color)
    if size:
        garments = garments.filter(size__icontains=size)
    if line:
        garments = garments.filter(line__icontains=line)

    context = {"garments": garments}
    return render(request, "tracking/waiting_folding.html", context)
