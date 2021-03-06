from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

from accounts.models import User, AdminDiv, Volunteer, Child, Manager, Organization
from accounts.serializers import VolunteerSerializer, ChildSerializer, ManagerSerializer, AdminDivSerializer, UserSerializer, PasswordSerializer, OrganizationSerializer


model2Serializer = {Volunteer: VolunteerSerializer,
                    Child: ChildSerializer,
                    Manager: ManagerSerializer}

class AccountsView(APIView):
    def get(self, request):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = model2Serializer[type(request.user.role_object)]
        serializer = serializer(instance=request.user.role_object, data=request.data, mode="change_personal_info")
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignView(APIView):
    def get(self, request):
        serializer = AuthTokenSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = serializer.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user.set_password(request.data["newPassword"])
            user.save()
            user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class OrganizationView(APIView):
    '''
    ??????????????????????????????????????????manager???????????????????????????
    '''
    def get(self, request):
        organization = Organization.objects.get(id=request.GET.get("id"))
        serializer = OrganizationSerializer(instance=organization)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def getList(self, request):
        organization = Organization.objects.filter(administrator=request.GET.get("id"))

    '''
    ??????????????????????????????????????????????????????manager????????????
    '''
    def post(self, request):
        data = request.data
        data["administrator"] = request.user.id
        serializer = OrganizationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        organization = Organization.objects.get(id=request.data.pop("id"))
        serializer = OrganizationSerializer(instance=organization, data=request.data, mode="change")
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        pass


#??????????????????: 
#??????????????????: switchAccess
#??????????????????: acceptApplication, cancelApplication
#????????????????????????: submitApplication
#??????????????????: exitOrg
#??????????????????: changeOrg
class StudentsAndOrganization(APIView):
    def switchAccess(self, request):
        organization = Organization.objects.get(id=request.data["id"])
        inviteCode = "1234" if organization.inviteCode == "" else ""
        organization.inviteCode = inviteCode
        organization.save()
        return Response({"inviteCode": inviteCode}, status=status.HTTP_200_OK)

    def submitApplication(self, request):
        pass

    def acceptApplication(self, request):
        pass

    def cancelApplication(self, request):
        pass

    def exitOrg(self, request):
        pass

    def changeOrg(self, request):
        pass


class AdminDivView(APIView):
    def get(self, request):
        adminDivs = AdminDiv.objects.all()
        serializer = AdminDivSerializer(instance=adminDivs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, reuest):
        serializer = AdminDivSerializer(data=reuest.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

