from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from accounts.models import Garment
from django.utils import timezone


@api_view(["GET"])
@permission_classes([HasAPIKey])
def get_garment_waiting_dryroom(request):
    rfid_garment = request.query_params.get("rfid_garment")
    buyer = request.query_params.get("buyer")
    style = request.query_params.get("style")
    wo = request.query_params.get("wo")
    color = request.query_params.get("color")
    size = request.query_params.get("size")
    line = request.query_params.get("line")

    garments = Garment.objects.filter(pqc_good__gt=0, dryroom_ci=0)

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

    data = list(
        garments.values(
            "id_garment",
            "rfid_garment",
            "item",
            "buyer",
            "style",
            "wo",
            "color",
            "size",
            "line",
            "pqc_good",
            "pqc_good_time",
            "dryroom_ci",
            "dryroom_ci_time",
        ).order_by("-pqc_good_time")
    )

    return Response({"success": True, "status": "waiting_dryroom", "count": len(data), "data": data})


@api_view(["GET"])
@permission_classes([HasAPIKey])
def get_garment_waiting_folding(request):
    rfid_garment = request.query_params.get("rfid_garment")
    buyer = request.query_params.get("buyer")
    style = request.query_params.get("style")
    wo = request.query_params.get("wo")
    color = request.query_params.get("color")
    size = request.query_params.get("size")
    line = request.query_params.get("line")

    garments = Garment.objects.filter(dryroom_co__gt=0, folding_ci=0)

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

    data = list(
        garments.values(
            "id_garment",
            "rfid_garment",
            "item",
            "buyer",
            "style",
            "wo",
            "color",
            "size",
            "line",
            "dryroom_co",
            "dryroom_co_time",
            "folding_ci",
            "folding_ci_time",
        ).order_by("-dryroom_co_time")
    )

    return Response({"success": True, "status": "waiting_folding", "count": len(data), "data": data})


@api_view(["POST"])
@permission_classes([HasAPIKey])
def dryroom_checkin_api(request):
    rfid_garment = (request.data.get("rfid_garment") or "").strip()

    if not rfid_garment:
        return Response({"success": False, "message": "rfid_garment wajib diisi."}, status=400)

    garment = Garment.objects.filter(rfid_garment=rfid_garment).first()
    if not garment:
        return Response({"success": False, "message": "Garment tidak ditemukan."}, status=404)

    if not (garment.pqc_good > 0 and garment.dryroom_ci == 0):
        return Response({"success": False, "message": "Dry Room Check In gagal. Pastikan PQC Good sudah ada dan belum pernah Check In Dry Room."}, status=400)

    garment.dryroom_ci = 1
    garment.dryroom_ci_time = timezone.now()
    garment.save(update_fields=["dryroom_ci", "dryroom_ci_time"])

    return Response(
        {
            "success": True,
            "message": "Dry Room Check In berhasil.",
            "rfid_garment": garment.rfid_garment,
            "dryroom_ci": garment.dryroom_ci,
            "dryroom_ci_time": garment.dryroom_ci_time,
        }
    )


@api_view(["POST"])
@permission_classes([HasAPIKey])
def dryroom_checkout_api(request):
    rfid_garment = (request.data.get("rfid_garment") or "").strip()

    if not rfid_garment:
        return Response({"success": False, "message": "rfid_garment wajib diisi."}, status=400)

    garment = Garment.objects.filter(rfid_garment=rfid_garment).first()
    if not garment:
        return Response({"success": False, "message": "Garment tidak ditemukan."}, status=404)

    if not (garment.dryroom_ci > 0 and garment.dryroom_co == 0):
        return Response({"success": False, "message": "Dry Room Check Out gagal. Pastikan garment sudah Check In Dry Room dan belum pernah Check Out."}, status=400)

    garment.dryroom_co = 1
    garment.dryroom_co_time = timezone.now()
    garment.save(update_fields=["dryroom_co", "dryroom_co_time"])

    return Response(
        {
            "success": True,
            "message": "Dry Room Check Out berhasil.",
            "rfid_garment": garment.rfid_garment,
            "dryroom_co": garment.dryroom_co,
            "dryroom_co_time": garment.dryroom_co_time,
        }
    )


@api_view(["POST"])
@permission_classes([HasAPIKey])
def folding_checkin_api(request):
    rfid_garment = (request.data.get("rfid_garment") or "").strip()

    if not rfid_garment:
        return Response({"success": False, "message": "rfid_garment wajib diisi."}, status=400)

    garment = Garment.objects.filter(rfid_garment=rfid_garment).first()
    if not garment:
        return Response({"success": False, "message": "Garment tidak ditemukan."}, status=404)

    if not (garment.dryroom_co > 0 and garment.folding_ci == 0):
        return Response({"success": False, "message": "Folding Check In gagal. Pastikan garment sudah Check Out Dry Room dan belum pernah Check In Folding."}, status=400)

    garment.folding_ci = 1
    garment.folding_ci_time = timezone.now()
    garment.save(update_fields=["folding_ci", "folding_ci_time"])

    return Response(
        {
            "success": True,
            "message": "Folding Check In berhasil.",
            "rfid_garment": garment.rfid_garment,
            "folding_ci": garment.folding_ci,
            "folding_ci_time": garment.folding_ci_time,
        }
    )


@api_view(["POST"])
@permission_classes([HasAPIKey])
def folding_checkout_api(request):
    rfid_garment = (request.data.get("rfid_garment") or "").strip()

    if not rfid_garment:
        return Response({"success": False, "message": "rfid_garment wajib diisi."}, status=400)

    garment = Garment.objects.filter(rfid_garment=rfid_garment).first()
    if not garment:
        return Response({"success": False, "message": "Garment tidak ditemukan."}, status=404)

    if not (garment.folding_ci > 0 and garment.folding_co == 0):
        return Response({"success": False, "message": "Folding Check Out gagal. Pastikan garment sudah Check In Folding dan belum pernah Check Out."}, status=400)

    garment.folding_co = 1
    garment.folding_co_time = timezone.now()
    garment.save(update_fields=["folding_co", "folding_co_time"])

    return Response(
        {
            "success": True,
            "message": "Folding Check Out berhasil.",
            "rfid_garment": garment.rfid_garment,
            "folding_co": garment.folding_co,
            "folding_co_time": garment.folding_co_time,
        }
    )


@api_view(["GET"])
@permission_classes([HasAPIKey])
def get_lines_overview_api(request):
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

    return Response({"success": True, "count": len(lines), "data": list(lines)})


@api_view(["GET"])
@permission_classes([HasAPIKey])
def get_line_detail_api(request, line):
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

    return Response({"success": True, "line": line, "summary": summary, "detail_data": detail_data})
