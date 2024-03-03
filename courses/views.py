from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .models import Product, Purchase, Group, Lesson
from .serializers import ProductSerializer, GroupSerializer, LessonSerializer, ProductStatisticsSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductPurchaseAPIView(generics.CreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        user = self.request.user
        purchase = Purchase.objects.create(user=user, product=product)
        existing_groups = Group.objects.filter(product=product)

        if not existing_groups.exists():
            new_group = self.create_group(product, user, 1)
            return Response({"message": "User added to the first group."}, status=200)
        else:
            for group in existing_groups:
                if group.students.count() < product.max_students:
                    group.students.add(user)
                    self.redistribute_students(product)
                    return Response({"message": "User added to an existing group."}, status=200)

            new_group_number = existing_groups.count() + 1
            new_group = self.create_group(product, user, new_group_number)
            return Response({"message": "User added to a new group."}, status=200)
        
    def create_group(self, product, user, group_number):
        new_group = Group.objects.create(product=product, name=f"{product.name} Group {group_number}")
        new_group.students.add(user)
        return new_group
    
    def redistribute_students(self, product):
        groups = Group.objects.filter(product=product)
        num_groups = len(groups)
        total_students = sum(group.students.count() for group in groups)
        ideal_students_per_group = total_students // num_groups
        excess_students = []

        for group in groups:
            difference = group.students.count() - ideal_students_per_group

            if difference > 0:
                excess = group.students.all()[:difference]
                excess_students.extend(excess)
                group.students.remove(*excess)

        while excess_students:
            for group in groups:
                if excess_students:
                    student = excess_students.pop()
                    group.students.add(student)
    

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        user = self.request.user
        try:
            product = Product.objects.get(id=product_id)
            if not self.has_access_to_product(user, product):
                return Lesson.objects.none()
        except Product.DoesNotExist:
            return Lesson.objects.none()

        queryset = Lesson.objects.filter(product=product)
        return queryset
    
    def has_access_to_product(self, user, product):
        return Purchase.objects.filter(user=user, product=product).exists()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You don't have access to this product or there are no lessons available."}, status=status.HTTP_403_FORBIDDEN)
    

class ProductStatisticsAPIView(generics.ListAPIView):
    serializer_class = ProductStatisticsSerializer

    def get_queryset(self):
        products = Product.objects.all()
        statistics = []
        total_users = User.objects.count()

        for product in products:
            groups_count = Group.objects.filter(product=product).count()
            max_students_per_group = product.max_students
            total_purchases = Purchase.objects.filter(product=product).count()
            access_percentage = (total_purchases / total_users) * 100 if total_users != 0 else 0

            if total_purchases and groups_count:
                average_fill_percentage = (total_purchases / (groups_count * max_students_per_group)) * 100
            else:
                average_fill_percentage = 0

            statistics.append({
                'product_name': product.name,
                'students_count': total_purchases,
                'groups_count': groups_count,
                'average_fill_percentage': average_fill_percentage,
                'access_percentage': access_percentage,
            })

        return statistics