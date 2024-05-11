from django.db import IntegrityError # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore

from auth_jwt.serializers import *

import random
from jwt_practice.settings import EMAIL_HOST_USER
from auth_jwt.tasks import *

#logout View
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
'''
CRUD OPERATIONS RELATED TO USER_ROLE_LIST STARTS HERE
'''
class UserRoleList(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,IsAdminUser)
    def post(self,request):
        serializer = UserRoleListSerializer(data = request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'status':201,'msg':'New user role created sucessfully!!'},status=201)
            else:
                return Response({'status':500,'error':str(serializer.errors)},status=500)
        except IntegrityError as e:
            return Response({'status':500,'error':str(e)},status=500)
    def put(self,request):
        id = request.data.get('id')
        print(f"role id from the front is {id}")
        try:
            user_role_list = UserRole.objects.get(id=id)
            serializer = UserRoleListSerializer(user_role_list,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':200,'msg':'user role updated'},status=200)
            else:
                return Response({'status':500,'error':str(serializer.errors)},status=500)
        except UserRole.DoesNotExist as e:
            return Response({'status':404,'error':str(e)},status=404)
    def delete(self,request):
        id = request.data.get('id')
        try:
            user_role_list = UserRole.objects.get(id=id)
            user_role_list.delete()
            return Response({'status':204,'msg':'user role list is deleted successfully!!'},status=204)
        except UserRole.DoesNotExist as e:
            return Response({'status':500,'error':str(e)},status=500)
    def get(self,request):
        user_role = UserRole.objects.all()
        serializer = UserRoleListSerializer(user_role,many=True)
        return Response({'status':200,'data':serializer.data},status=200)
'''
CRUD OPERATIONS RELATED TO USER_ROLE_LIST ENDS HERE
'''
otp = {}
data_global = {}
class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.save()

            role_id = request.data.get('role')
            if role_id:
                role = UserRole.objects.get(id=role_id)
                userProfileSerializer  = UserProfileSerializer(data = {'user' : user.id,'role':role_id,'role_name':role.role_list})
                if userProfileSerializer.is_valid():
                    userProfileSerializer.save() 
                    OTP = random.randint(0,999999)
                    otp.clear()
                    otp.update({"otp":OTP})
                    print(f"saved otp : {otp}")
                    # user = request.data.get('user')
                    username = user.username
                    email_ = user.email
                    data_global.clear()
                    data_global.update({"username":f"{username}", "email":f"{email_}",'role_id':role_id})
                    print(f"saved user : {data_global}")
                    # send otp via email using celery
                    try:
                        email_addr = data_global['email']
                        subject = f"{data_global['username']} please verify OTP"
                        message = "verify your OTP " + str(otp['otp'])
                        recipient_list = [email_addr]     
                        send_email_task.delay(subject, message, EMAIL_HOST_USER, recipient_list)
                        email_addr=""                    
                        return Response({'status':200,'msg':'Email sent!!'},status=200)# email sent
                    except:
                        return Response({'status':400,'error':'Something went wrong while sending email'},status=400)
                else:
                    user.delete()
                    return Response({'status':500,'error':str(userProfileSerializer.errors)},status=500)
            else:
                user.delete()
                return Response({'status':404,'error':'user role not found'},status=404)
        else:
            user.delete()
            return Response({'status':500,'error':str(serializer.errors)},status=500)
class EmailVerification(APIView):
    def post(self,request):
        OTP = request.data.get('otp')
        print(f"otp from front : {OTP} otp saved from before : {otp['otp']}")
        try:
            if int(OTP) == int(otp['otp']):
                try:
                    username = data_global['username']
                    user = User.objects.get(username=username)
                    user.is_active = True
                    user.save()
                    return Response({'status':200,'msg':'user account verified'},status=200)
                except User.DoesNotExist as e:
                    return Response({'status':404,'error':str(e)},status=404)
            else:
                return Response({'status':500,'error':'otp did nor match'},status=500)
        except Exception as e:
            return Response({'status':500,'error':str(e)},status=500)
# from rest_framework_simplejwt.tokens import RefreshToken
class LogoutView(APIView):
     authentication_classes = (JWTAuthentication,)
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response({'status':205,'msg':'user logged out refresh token reset'},status=205)
          except Exception as e:
               return Response({'status':400,'error':str(e)},status=400)
class homeView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        role_id = user_profile.role.id
        role_name = user_profile.role.role_list
        user_data = {
            'username':user.username,
            'email':user.email,
            'role_id':role_id,
            'role_name':role_name
        }
        return Response({'status':200,'data':user_data},status=200)