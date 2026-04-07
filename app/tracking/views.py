from django.shortcuts import render
from accounts.models import Garment


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
