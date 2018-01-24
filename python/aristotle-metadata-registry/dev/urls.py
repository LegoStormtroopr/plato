"""
URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
"""
from django.conf.urls import url, include
from django.contrib.staticfiles import views
from django.conf import settings
from django.conf.urls.static import static
# from django_spaghetti.views import PlateView, SingleAppPlate, SingleModelPlate


urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True) + [
    # url(r'^static/(?P<path>.*)$', views.serve),
    url(r'^', include('aristotle_mdr.urls')),
    url(r'^browse/', include('aristotle_mdr.contrib.browse.urls')),
    url(r'^help/', include('aristotle_mdr.contrib.help.urls', app_name="aristotle_help", namespace="aristotle_help")),
#     url(r'^labs/plate/$', PlateView.as_view(
#         # apps = ['aristotle_mdr'],
#         vis_options = {
#         "edges": {
#           "smooth": {
#             "type": "cubicBezier",
#             "roundness": 0.55
#           }
#         },
#         # "interaction": {
#         #   "tooltipDelay":99999,
#         #   "navigationButtons":True,
#         #   "dragNodes":False,
#         # },
#         "layout": {
#             'hierarchical': {
#                 'sortMethod': 'directed',
#                 'direction':'UD'
#             }
#         }
#       }
    
#         ), name='plate'),
#     url(r'^labs/plate/(?P<app_label>.+)/(?P<model_name>.+)', SingleModelPlate.as_view(
#         apps = '__all__',
#         override_settings = {'exclude': {}},
#     )),
#     url(r'^labs/plate/(?P<app_label>.+)', SingleAppPlate.as_view())
]

# urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
