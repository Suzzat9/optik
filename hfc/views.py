from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UploadSerializer
import pandas as pd
from .hfc_checks import *


class UploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadSerializer

    def get(self, request, *args, **kwargs):
        return render(request, "upload.html")

    def post(self, request, *args, **kwargs):
        try:
            data = request.FILES
            serializer = self.serializer_class(data=request.FILES)
            if not serializer.is_valid():
                return Response(
                    {"status": False, "message": "Provide a valid file type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            datafile = data.get("file_uploaded")
            print(datafile.content_type)
            if datafile:
                df = pd.read_excel(datafile)
                duplicates(df, 0)
                # results.html
                return Response(
                    {"status": True, "message": "File successfully read"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"status": False, "message": "No file was uploaded"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": str(
                        "We could not process this file, " + "ERROR: " + str(e)
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
