from rest_framework.views import APIView
from .serializers import AddItemSerializer, UserSerializer
from rest_framework.response import Response
from .models import Item
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated


class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the user
            # You may want to perform additional operations such as sending a verification email here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication successful, generate JWT tokens
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            # Log in the user
            login(request, user)
            return Response(
                {
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            # If authentication fails, return an error response
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class AddItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = AddItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateItem(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            message = {"message": "Item does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer = AddItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            message = {"message": "Item does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        item.delete()
        message = {"message": "Successfully deleted the item."}
        return Response(message, status=status.HTTP_204_NO_CONTENT)


class BillGeneration(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        item_ids = request.data.get("item_ids", [])

        found_items = []
        not_found_ids = []

        for item_id in item_ids:
            try:
                # Try to retrieve the item from the database based on the ID
                item = Item.objects.get(id=item_id)
                # If the item is found, add it to the list of found items
                found_items.append(item)
            except Item.DoesNotExist:
                # If the item is not found, add its ID to the list of not found IDs
                not_found_ids.append(item_id)

        total_cost = sum(item.item_price for item in found_items)

        # Return the total cost and the list of not found IDs in the response
        response_data = {"total_cost": total_cost, "not_found_ids": not_found_ids}
        return Response(response_data, status=status.HTTP_200_OK)
