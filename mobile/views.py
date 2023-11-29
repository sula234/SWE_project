from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from mobile.models import Dispatcher
from mobile.serializers import DriverSerializer, UserSerializer, RouteSerializer, FuelingSerializer, \
    FuelingReportSerializer
from users.models import User, Driver, Route, FuelPreson, FuelReport
from users.views import Routes
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['POST'])
def signup(request):
    serializer = DriverSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def login(request):
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        return Response({"detail": "Incorrect credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    #   serializer = UserSerializer(user)
    return Response({'token': token.key})


@csrf_exempt
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")


@csrf_exempt
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def routes(request):
    # Access the user from the request
    user = request.user
    driver = Driver.objects.get(user=user)
    routess = Route.objects.filter(driver=driver)

    serializer = RouteSerializer(routess, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_route(request, route_id):
    try:
        user = request.user
        driver = Driver.objects.get(user=user)
        route = Route.objects.get(id=route_id, driver=driver)
    except Route.DoesNotExist:
        return Response({'detail': 'Route not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # For a full update
        serializer = RouteSerializer(route, data=request.data)
    else:
        # For a partial update "PATCH"
        serializer = RouteSerializer(route, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def driver_info(request):
    # Access the user from the request
    user = request.user
    driver = Driver.objects.get(user=user)

    serializer = DriverSerializer(driver)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def fueling_info(request):
    # Access the user from the request
    user = request.user
    fueling = FuelPreson.objects.get(user=user)
    serializer = FuelingSerializer(fueling)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def fueling_reports(request):
    # Access the user from the request
    user = request.user
    fuelPERDUN = FuelPreson.objects.get(user=user)
    fuel_reports = FuelReport.objects.filter(fuel_preson=fuelPERDUN)
    serializer = FuelingReportSerializer(
        # driver_name = fuel_reports.driver.first_name,
        # vehicle_plate_number = fuel_reports.vehicle.license_plate,
        fuel_reports, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_fueling_report(request, fueling_report_id):
    try:
        user = request.user
        fuelPERDUN = FuelPreson.objects.get(user=user)
        fueling = FuelReport.objects.get(id=fueling_report_id, fuel_preson=fuelPERDUN)
    except FuelReport.DoesNotExist:
        return Response({'detail': 'Route not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # For a full update
        serializer = FuelingReportSerializer(fueling, data=request.data)
    else:
        # For a partial update "PATCH"
        serializer = FuelingReportSerializer(fueling, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dispatcher_number(request):
    settings = Dispatcher.objects.first()  # THERE SHOULD BE ONLY 1 INSTANCE OF DISPATCHER
    return Response({'dispatcher_phone_number': settings.dispatcher_phone_number})

