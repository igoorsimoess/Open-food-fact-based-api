# Create your views here.
from .models import FoodTable
from .serializers import FoodTableSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from utils.openfood import FoodData
from rest_framework.response import Response
from rest_framework import status, views
from datetime import datetime
from .serializers import APIInfoSerializer
from django.db import connection
import psutil
import os
from system import start_time


class FoodTableViewSet(ModelViewSet, PageNumberPagination):
    queryset = FoodTable.objects.all()
    serializer_class = FoodTableSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = None

        if self.action == "list":
            queryset = FoodTable.objects.all()

            return queryset

        elif self.action == "retrieve":
            pk = self.kwargs["pk"]
            updated_data = self.get_updated_data()
            if updated_data:
                try:
                    queryset = FoodTable.objects.get(code=pk)
                except:
                    queryset = None

                # Update the fields of the instance using the updated_data
                for key, value in updated_data.items():
                    setattr(queryset, key, value)

                queryset.save()

                queryset = FoodTable.objects.get(code=pk)

                return queryset
            else:
                return queryset  # None

        elif self.action == "update":
            pk = self.kwargs["pk"]
            updated_data = self.get_updated_data()
            if updated_data:
                queryset = FoodTable.objects.get(code=pk)

                # Update the fields of the instance using the updated_data
                for key, value in updated_data.items():
                    setattr(queryset, key, value)

                queryset.save()

                queryset = FoodTable.objects.get(code=pk)

                return queryset
            else:
                return queryset  # None

        elif self.action == "destroy":
            pk = self.kwargs["pk"]

            queryset = FoodTable.objects.filter(code=pk)

            return queryset

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FoodTableSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = FoodTableSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        try:
            if queryset is None:
                raise FoodTable.DoesNotExist
            serializer = FoodTableSerializer(queryset)
            return Response(serializer.data)

        except FoodTable.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        queryset = self.get_queryset()
        try:
            if queryset is None:
                raise FoodTable.DoesNotExist

            serializer = FoodTableSerializer(queryset, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()

        try:
            updated_data = {}
            updated_data["status"] = "trash"

            queryset.update(**updated_data)
            serializer = FoodTableSerializer(queryset, many=True)

            return Response(serializer.data)

        except FoodTable.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_updated_data(self):
        data = FoodData(self.kwargs["pk"])

        updated_data = data.get_data()
        return updated_data


class APIInformationView(views.APIView):
    def get(self, request):
        db_connection = self.get_db_connection()
        memory = self.get_memory_usage()
        uptime = self.get_api_running_time(start_time=start_time)
        data = {
            "db_connection": db_connection,
            "last_cron_exec": datetime.now(),  # didn't need to schedule any task for now.
            "running_time": uptime,
            # 'running_time': datetime.now(),
            "memory_usage": memory,
        }
        try:
            self.get_db_connection
        except Exception as error:
            print(error)
        serializer = APIInfoSerializer(data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_memory_usage(self):
        pid = os.getpid()
        process = psutil.Process(pid)
        memory = process.memory_info()

        memory_used_in_mb = memory.rss / (1024**2)

        return f"{memory_used_in_mb:.2f} Mb"

    def get_db_connection(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except Exception:
            return False

    def get_cron_usage(self):
        return datetime.now()

    def get_api_running_time(self, start_time):
        time_now = datetime.now()
        up_time = time_now - start_time

        formatted_time = str(up_time).split(".")[0]
        print(formatted_time)

        return formatted_time
