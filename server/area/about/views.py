from django.shortcuts import render
from rest_framework.response import Response
import json
from rest_framework import generics, permissions
from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema

class AboutJson(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = None

    @swagger_auto_schema(
        operation_id="about_json",
        operation_description="Get about.json",
        responses={200: "about.json"},
    )
    def get(self, request):
        try:
            file = open("about/about.json", "r")
            data = json.load(file)
            file.close()
            return Response(data)
        except:
            return Response({"error": "error while reading about.json"})

class RootRedirect(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_id="root_redirect",
        operation_description="Redirect to about.json",
        responses={200: "about.json"},
    )
    def get(self, request):
        return redirect("/about.json")
