from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserVerifySerializer
from .emails import send_otp
from .models import User
from datetime import *
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class GenerateOtpAPI(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

        if User.objects.filter(email=serializer.data['email']).exists():

            user = User.objects.get(email=serializer.data['email'])

            #if login is restricted
            if user.login_restricted is not None:
                if (datetime.now(timezone.utc) < user.login_restricted):
                    return Response({'message' : "Login has been restricted for 1 hour "},
                                    status = status.HTTP_400_BAD_REQUEST)
                
            #if another OTP requested under 1 min
            if  user.otp_created is not None:
                if datetime.now(timezone.utc) < (user.otp_created + timedelta(minutes=1)) :
                    return Response({'message' : "Wait one minute to make another OTP request"},
                                    status= status.HTTP_400_BAD_REQUEST,)
            
            #if no terminating conditions
            send_otp(serializer.data['email'])
            return Response({'message' : 'OTP sent on mail ','data' : serializer.data,},
                            status = status.HTTP_200_OK)
        
        #if internal server or not enough parameters
        return Response({'message' : "Something went wrong "},
                        status= status.HTTP_400_BAD_REQUEST)

class VerifyOtpAPI(APIView):
    def post(self,request):
        serializer = UserVerifySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data['email']
            otp = serializer.data['otp']
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # if email is wrong
                return Response({'message' : "Email not found "},
                                status = status.HTTP_400_BAD_REQUEST)
            
            #if login is restricted
            if user.login_restricted is not None:
                if (datetime.now(timezone.utc) < user.login_restricted):
                    return Response({'message' : "Login has been restricted for 1 hour "},
                                    status = status.HTTP_400_BAD_REQUEST)
                
            # if entered otp is wrong
            if not user.otp == otp:
                user.otp_fails = user.otp_fails + 1
                user.save()
                if user.otp_fails == 5:
                    user.login_restricted = datetime.now(timezone.utc) + timedelta(hours=1)
                    return Response({'message' : "Login has been restricted for 1 hour "},
                                    status = status.HTTP_400_BAD_REQUEST)

                return Response({'message' : "OTP Mismatch "},
                                status = status.HTTP_400_BAD_REQUEST) 

            # otp time out
            if user.otp_created + timedelta(minutes=5) < datetime.now(timezone.utc):
                return Response({'message' : "Unsuccessfull ! OTP TIME OUT"},
                                status = status.HTTP_400_BAD_REQUEST)


            # if successful
            token = get_tokens(user)
            user.otp_fails=0
            
            return Response({'message' : 'OTP verified successfully ','token' : token,},
                            status = status.HTTP_200_OK)
        
        return Response({'message' : "Something went wrong!"},
                        status= status.HTTP_400_BAD_REQUEST)
            