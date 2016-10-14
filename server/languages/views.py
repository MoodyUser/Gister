import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
# Create your views here.
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
# Serializers define the API representation.
from rest_framework import serializers, viewsets
# ViewSets define the view behavior.
from .models import Languages


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Languages
        fields = ('id',
                  'title',
                  'icon',
                  'file_ending',
                  'parent',
                  'description',
                  )


@authentication_classes((SessionAuthentication, TokenAuthentication))
class LanguageViewSet(viewsets.ModelViewSet):
    def filter_queryset(self, queryset):
        # Getting the arguments.
        query_string = self.request.GET
        if 'parent' in query_string:
            queryset = queryset.filter(parent__isnull=True).all()
        return super(LanguageViewSet, self).filter_queryset(queryset)
    
    queryset = Languages.objects.all()
    serializer_class = LanguageSerializer
