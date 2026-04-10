from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import Garment
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone


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


@login_required
def dryroom_transaction_page(request):
    if request.method == "POST":
        action = request.POST.get("action")
        rfid_garment = request.POST.get("rfid_garment", "").strip()

        if not rfid_garment:
            messages.error(request, "RFID garment wajib diisi.")
            return redirect("dryroom_transaction_page")

        garment = Garment.objects.filter(rfid_garment=rfid_garment).first()

        if not garment:
            messages.error(request, f"Garment RFID {rfid_garment} tidak ditemukan.")
            return redirect("dryroom_transaction_page")

        now = timezone.now()

        if action == "checkin":
            if garment.pqc_good > 0 and garment.dryroom_ci == 0:
                garment.dryroom_ci = 1
                garment.dryroom_ci_time = now
                garment.save(update_fields=["dryroom_ci", "dryroom_ci_time"])
                messages.success(request, f"Dry Room Check In berhasil untuk RFID {rfid_garment}.")
            else:
                messages.error(request, "Dry Room Check In gagal. Pastikan PQC Good sudah ada dan belum pernah Check In Dry Room.")

        elif action == "checkout":
            if garment.dryroom_ci > 0 and garment.dryroom_co == 0:
                garment.dryroom_co = 1
                garment.dryroom_co_time = now
                garment.save(update_fields=["dryroom_co", "dryroom_co_time"])
                messages.success(request, f"Dry Room Check Out berhasil untuk RFID {rfid_garment}.")
            else:
                messages.error(request, "Dry Room Check Out gagal. Pastikan garment sudah Check In Dry Room dan belum pernah Check Out.")

        else:
            messages.error(request, "Action tidak valid.")

        return redirect("dryroom_transaction_page")

    return render(request, "tracking/dryroom_transaction.html")


@login_required
def folding_transaction_page(request):
    if request.method == "POST":
        action = request.POST.get("action")
        rfid_garment = request.POST.get("rfid_garment", "").strip()

        if not rfid_garment:
            messages.error(request, "RFID garment wajib diisi.")
            return redirect("folding_transaction_page")

        garment = Garment.objects.filter(rfid_garment=rfid_garment).first()

        if not garment:
            messages.error(request, f"Garment RFID {rfid_garment} tidak ditemukan.")
            return redirect("folding_transaction_page")

        now = timezone.now()

        if action == "checkin":
            if garment.dryroom_co > 0 and garment.folding_ci == 0:
                garment.folding_ci = 1
                garment.folding_ci_time = now
                garment.save(update_fields=["folding_ci", "folding_ci_time"])
                messages.success(request, f"Folding Check In berhasil untuk RFID {rfid_garment}.")
            else:
                messages.error(request, "Folding Check In gagal. Pastikan garment sudah Check Out Dry Room dan belum pernah Check In Folding.")

        elif action == "checkout":
            if garment.folding_ci > 0 and garment.folding_co == 0:
                garment.folding_co = 1
                garment.folding_co_time = now
                garment.save(update_fields=["folding_co", "folding_co_time"])
                messages.success(request, f"Folding Check Out berhasil untuk RFID {rfid_garment}.")
            else:
                messages.error(request, "Folding Check Out gagal. Pastikan garment sudah Check In Folding dan belum pernah Check Out.")

        else:
            messages.error(request, "Action tidak valid.")

        return redirect("folding_transaction_page")

    return render(request, "tracking/folding_transaction.html")
