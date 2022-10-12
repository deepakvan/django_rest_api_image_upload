from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from .Serializer import UserSerializer, UserImageSerializer,RegisterSerializer
from .models import UserImages
from django.contrib.auth.models import User


@csrf_exempt
@api_view(["POST","GET"])
@permission_classes((AllowAny,))
def login(request):
    if request.method=="POST":
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},status=status.HTTP_200_OK)
    serializer = UserSerializer()
    return Response(serializer.data)


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    Response.status_code=status.HTTP_200_OK
    return Response(data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET','POST'])
def upload_image(request):
    if request.method=="POST":
        token_value = get_authorization_header(request).decode('utf-8')
        if token_value is None or token_value == "null" or token_value.strip() == "":
            return Response({"Error": 'Authorization Header or Token is missing on Request Headers'})
        print(token_value, type(token_value))
        try:
            #raise error if token not found
            #Token.objects.get(key=request.data['token']).user
            Token.objects.get(key=token_value.split(" ")[-1]).user_id
        except Token.DoesNotExist:
            return Response({"Error":"Token is invalid or expired"},status=status.HTTP_404_NOT_FOUND)
        user_id = Token.objects.get(key=token_value.split(" ")[-1]).user_id
        user=User.objects.get(pk=user_id)
        image=UserImages(name=request.data["name"],path=request.data["path"],user=user)
        if image.type_check() and image.size_check():
            image.save()
            return Response({"success":"Image saved successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":"file must be an image and size less then 500kb"},status=status.HTTP_400_BAD_REQUEST)
    serializer = UserImageSerializer()
    return Response(serializer.data)



@csrf_exempt
@api_view(["POST","GET"])
@permission_classes((AllowAny,))
def register(request):
    if request.method=="POST":
        name= request.data.get("name")
        username = request.data.get("username")
        password = request.data.get("password")
        if name is None or username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        existing_user=User.objects.filter(username=username).first()
        if existing_user:
            return Response({"error":"Username is already taken"},status=status.HTTP_409_CONFLICT)
        if len(password) >= 8:
            user = User.objects.create_user(first_name=name, username=username, password=password)
            user.save()
            return Response({"success": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"password must be atleast 8 character long."})
    serializer = RegisterSerializer()
    return Response(serializer.data)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def all(request):
    token_value = get_authorization_header(request).decode('utf-8')
    if token_value is None or token_value == "null" or token_value.strip() == "":
        return Response({"Error": 'Authorization Header or Token is missing on Request Headers'})
    # print(token_value, type(token_value))
    try:
        # raise error if token not found
        # Token.objects.get(key=request.data['token']).user
        Token.objects.get(key=token_value.split(" ")[-1]).user_id
    except Token.DoesNotExist:
        return Response({"Error": "Token is invalid or expired"}, status=status.HTTP_404_NOT_FOUND)
    user_id = Token.objects.get(key=token_value.split(" ")[-1]).user_id
    user = User.objects.get(pk=user_id)
    all_images=user.userimages_set.all()
    print(all_images)
    ret_dict={}
    for image in all_images:
        print(image)
        ret_dict[image.id]={"name":image.name,"path":image.path.url}
    return Response(ret_dict)