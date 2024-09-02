# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import parcel_order
from .serializers import ItemSerializer
import random, string, uuid, re
from datetime import datetime
from django.utils.dateparse import parse_datetime

@api_view(['GET'])
def get_tracking_number(request):
    required_param_fields = ["origin_country_id", "destination_country_id", "weight", "created_at", "customer_id",
                             "customer_name", "customer_slug"]
    origin_country_id = request.query_params.get('origin_country_id')
    destination_country_id = request.query_params.get('destination_country_id')
    weight = request.query_params.get('weight')
    created_at = request.query_params.get('created_at')
    customer_id = request.query_params.get('customer_id')
    customer_name = request.query_params.get('customer_name')
    customer_slug = request.query_params.get('customer_slug')

    # check if all request parameters are present
    missing_params = [
        param
        for param in required_param_fields
        if param not in request.query_params
    ]
    if missing_params:
        return Response(
            {
                "error": f"Missing required query params: {', '.join(missing_params)}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    #check if origin_country_id has XX format
    try:
        origin_country_id = origin_country_id.upper()
        destination_country_id = destination_country_id.upper()
        if re.fullmatch(r'[A-Z]{2}', origin_country_id) is None or re.fullmatch(r'[A-Z]{2}', destination_country_id) is None:
            raise ValueError
    except ValueError:
        return Response({'error': 'Invalid country code. Country code should have 2 letters only'}, status=status.HTTP_400_BAD_REQUEST)

    # check if create_at is a valid datetime format
    try:
        parse_datetime(created_at)
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

    # check if weight is a valid datetime format
    try:
        weight = float(weight)
        if weight <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return Response({'error': 'Invalid weight. Give positive number'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        uuid.UUID(customer_id)
    except ValueError:
        return Response({'error': 'Invalid customer_id format'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate unique tracking number
    tracking_number, tn_created_at = generate_tracking_number()

    print(tracking_number)
    # save order object to database
    parcel_order.objects.create(
        origin_country_id=origin_country_id,
        destination_country_id=destination_country_id,
        weight=weight,
        order_created_at=parse_datetime(created_at),
        trackingNo_created_at = tn_created_at,
        customer_id=uuid.UUID(customer_id),
        customer_name=customer_name,
        customer_slug=customer_slug,
        tracking_number=tracking_number
    )

    response_data = {
        'tracking_number': tracking_number,
        'created_at': tn_created_at
    }
    serializer = ItemSerializer(data = response_data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response({'error': 'Error generating response'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_tracking_number():
    while True:
        tracking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        tn_created_at = datetime.now().isoformat()
        if not parcel_order.objects.filter(tracking_number=tracking_number).exists():
            return tracking_number, tn_created_at
