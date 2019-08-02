from cms.utils import get_language_from_request
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser
from Blogging.models import Blogs
from rest_framework import mixins
from rest_framework.views import APIView
from shop.serializers.Blogserializer import BloggingSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from rest_framework.reverse import reverse


class BlogList(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/Blogs/displayblogs.html'
    model = Blogs

    def get(self, request):
      queryset = Blogs.objects.all()
      return Response({'blogging': queryset})



class BlogRetrieveView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = Blogs.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'blogging': self.object}, template_name='shop/Blogs/displayblogs.html')



