from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import Garment
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q


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


@login_required
def line_overview_page(request):
    lines = (
        Garment.objects.exclude(line__isnull=True)
        .exclude(line__exact="")
        .values("line")
        .annotate(
            sewing_output=Count("id_garment", filter=Q(output__gt=0)),
            good_qc=Count("id_garment", filter=Q(qc_good__gt=0)),
            reject_qc=Count("id_garment", filter=Q(qc_reject__gt=0)),
            rework_qc=Count("id_garment", filter=Q(qc_rework__gt=0)),
            wira_qc=Count("id_garment", filter=Q(qc_rework__gt=0) & Q(qc_good=0) & Q(qc_reject=0)),
            good_pqc=Count("id_garment", filter=Q(pqc_good__gt=0)),
            reject_pqc=Count("id_garment", filter=Q(pqc_reject__gt=0)),
            rework_pqc=Count("id_garment", filter=Q(pqc_rework__gt=0)),
            wira_pqc=Count("id_garment", filter=Q(pqc_rework__gt=0) & Q(pqc_good=0) & Q(pqc_reject=0)),
        )
        .order_by("line")
    )

    context = {"lines": lines}
    return render(request, "tracking/line_overview.html", context)

@login_required
def line_detail_page(request, line):
    garments = Garment.objects.filter(line=line)

    summary = garments.aggregate(
        sewing_output=Count("id_garment", filter=Q(output__gt=0)),
        good_qc=Count("id_garment", filter=Q(qc_good__gt=0)),
        reject_qc=Count("id_garment", filter=Q(qc_reject__gt=0)),
        rework_qc=Count("id_garment", filter=Q(qc_rework__gt=0)),
        wira_qc=Count("id_garment", filter=Q(qc_rework__gt=0) & Q(qc_good=0) & Q(qc_reject=0)),
        good_pqc=Count("id_garment", filter=Q(pqc_good__gt=0)),
        reject_pqc=Count("id_garment", filter=Q(pqc_reject__gt=0)),
        rework_pqc=Count("id_garment", filter=Q(pqc_rework__gt=0)),
        wira_pqc=Count("id_garment", filter=Q(pqc_rework__gt=0) & Q(pqc_good=0) & Q(pqc_reject=0)),
    )

    detail_fields = [
        "rfid_garment",
        "rfid_iron",
        "rfid_qc",
        "rfid_pqc",
        "item",
        "buyer",
        "style",
        "wo",
        "color",
        "size",
    ]

    detail_data = {
        "sewing_output": list(garments.filter(output__gt=0).values(*detail_fields).order_by("rfid_garment")),
        "reject_qc": list(garments.filter(qc_reject__gt=0).values(*detail_fields).order_by("rfid_garment")),
        "rework_qc": list(garments.filter(qc_rework__gt=0).values(*detail_fields).order_by("rfid_garment")),
        "wira_qc": list(garments.filter(qc_rework__gt=0, qc_good=0, qc_reject=0).values(*detail_fields).order_by("rfid_garment")),
        "good_qc": list(garments.filter(qc_good__gt=0).values(*detail_fields).order_by("rfid_garment")),
        "reject_pqc": list(garments.filter(pqc_reject__gt=0).values(*detail_fields).order_by("rfid_garment")),
        "rework_pqc": list(garments.filter(pqc_rework__gt=0).values(*detail_fields).order_by("rfid_garment")),
        "wira_pqc": list(garments.filter(pqc_rework__gt=0, pqc_good=0, pqc_reject=0).values(*detail_fields).order_by("rfid_garment")),
        "good_pqc": list(garments.filter(pqc_good__gt=0).values(*detail_fields).order_by("rfid_garment")),
    }

    context = {
        "line": line,
        "summary": summary,
        "detail_data": detail_data,
    }
    return render(request, "tracking/line_detail.html", context)
