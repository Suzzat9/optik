from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UploadSerializer
from .forms import DataDetails
import pandas as pd
from django.http import HttpResponse
from .hfc_checks import *
from json import loads, dumps


def upload_datafile(request, *args, **kwargs):
    """
    Uploading required information and the datafile to be analysed
    """
    context = {}
    if request.POST:
        form = DataDetails(request.POST, request.FILES)
        if form.is_valid():
            datadetails = form.cleaned_data
            respondent_id = datadetails.get("respondent_id_field")
            surveyor_id = datadetails.get("surveyor_id_field")
            date = datadetails.get("date_field")
            start_time = datadetails.get("start_time_field")
            end_time = datadetails.get("end_time_field")
            min_duration = datadetails.get("min_duration_mins")
            max_duration = datadetails.get("max_duration_mins")
            categorical_vars = datadetails.get("categorical_fields")
            datafile = request.FILES["file"]
            if datafile:
                df = pd.read_excel(datafile)
                # Duplicate surveys
                res1 = duplicates(
                    df, respondent_id, surveyor_id, date, start_time, end_time
                )
                # Short and long surveys
                res2, res3 = short_long_surveys(df, respondent_id, surveyor_id, date, 
                       start_time, end_time, min_duration, max_duration)
                # Plotting categorical variables
                categ_vars = get_vars(categorical_vars)
                categ_charts = {}
                for i, var in enumerate(categ_vars):
                    categ_charts[var] = {"id" : i, "data" : loads(prep_categorical_variable(df, var))}

                #print(categ_charts)
                   
                # Store the result in session
                analysis_results = {
                    "duplicates" : res1.to_html(classes="table table-striped", index=False),
                    "long_surveys" : res2.to_html(classes="table table-striped", index=False),
                    "short_surveys": res3.to_html(classes="table table-striped", index=False),
                    "categorical_charts" : categ_charts
                }
                request.session["analysis_results"] = analysis_results
                # Redirect to the result view
                return redirect("/analysis-result")
        else:
            context["form"] = form
    else:  # its a GET request
        form = DataDetails()
        context["form"] = form

    return render(request, "upload.html", context)


def analysis_result(request, *args, **kwargs):
    # Retrieve the analysis result from session
    analysis_results = request.session.get("analysis_results")

    if not analysis_results:
        return HttpResponse("No analysis data found.")

    # Pass the result to the template context
    context = {"duplicates": analysis_results["duplicates"],
               "long_surveys" : analysis_results["long_surveys"],
               "short_surveys": analysis_results["short_surveys"],
               "categorical_charts" : analysis_results["categorical_charts"]}

    return render(request, "results.html", context)


# class UploadAPIView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     serializer_class = UploadSerializer

#     def get(self, request, *args, **kwargs):
#         return render(request, "upload.html")

#     def post(self, request, *args, **kwargs):
#         try:
#             # data = request.FILES
#             # serializer = self.serializer_class(data=request.FILES)
#             # if not serializer.is_valid():
#             #     return Response(
#             #         {"status": False, "message": "Provide a valid file type"},
#             #         status=status.HTTP_400_BAD_REQUEST,
#             #     )
#             # datafile = data.get("file_uploaded")
#             # print(datafile.content_type)
#             # Form to capture dataset details
#             form = DataDetails(request.POST, request.FILES)
#             if form.is_valid():
#                 datadetails = form.cleaned_data
#                 respondent_id = datadetails.get("respondent_id_field")
#                 surveyor_id = datadetails.get("surveyor_id_field")
#                 date = datadetails.get("date_field")
#                 start_time = datadetails.get("start_time_field")
#                 end_time = datadetails.get("end_time_field")
#                 datafile = request.FILES["file"]
#             else:
#                 form = DataDetails()
#             if datafile:
#                 df = pd.read_excel(datafile)
#                 duplicates(df, 0)
#                 # results.html
#                 return Response(
#                     {"status": True, "message": "File successfully read"},
#                     status=status.HTTP_201_CREATED,
#                 )
#             return Response(
#                 {"status": False, "message": "No file was uploaded"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         except Exception as e:
#             return Response(
#                 {
#                     "status": False,
#                     "message": str(
#                         "We could not process this file, " + "ERROR: " + str(e)
#                     ),
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
