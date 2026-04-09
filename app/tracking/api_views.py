from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from accounts.models import Garment


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
