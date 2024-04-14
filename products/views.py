from rest_framework import viewsets, permissions
from knox.auth import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category, Unit, ProductImage
from .serializers import ProductSerializer, CategorySerializer, UnitSerializer, ProductImageSerializer
from utils.pagination import CustomNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from utils.permissions import IsAdminOrOwner
from rest_framework.exceptions import ValidationError


# ! IF any changes later , Make this is a template for the new viewsets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = None

    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return super().get_permissions()

    class Meta:
        ordering = ["id"]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = None

    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return super().get_permissions()

    class Meta:
        ordering = ["id"]


# ! Separate it for admin and user or handle both efficiently
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CustomNumberPagination

    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get("category", None)
        if category:
            queryset = queryset.filter(category=category)
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request.user.id
        return super().create(request, *args, **kwargs)

    class Meta:
        ordering = ["id"]


# ! Check permissions for this action and handle it efficiently
class ProductImagesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        images_data = request.data.getlist("images")
        print("Product ID: ", product_id, "\n" * 4)
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": _("Product does not exist.")}, status=status.HTTP_404_NOT_FOUND)

        for image_data in images_data:
            serializer = ProductImageSerializer(data={"product": product_id, "image": image_data})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": _("Images assigned to product successfully.")}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        image_ids = request.data.get("image_ids", [])

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": _("Product does not exist.")}, status=status.HTTP_404_NOT_FOUND)

        if image_ids:
            # Deleting images from the product
            for image_id in image_ids:
                print("Image ID: ", image_id, "\n" * 4)
                try:
                    image = ProductImage.objects.get(pk=image_id, product_id=product_id)
                    image.delete()
                except ProductImage.DoesNotExist:
                    continue
                    # return Response({"error": _("Image does not exist.")}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": _("Images deleted from product successfully.")}, status=status.HTTP_200_OK)

        else:
            raise ValidationError({"error": _("No image IDs provided to delete from product.")})
