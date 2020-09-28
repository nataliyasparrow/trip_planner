from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^/dashboard$', views.dashboard),
    url(r'^/new$', views.new_item),
    url(r'^/create$', views.create_item),
    url(r'^/show_item$', views.show_item),
    url(r'^/(?P<id>\d+)$', views.show_info),
    url(r'^/edit/(?P<id>\d+)$', views.edit_item),
    url(r'^/update/(?P<id>\d+)$', views.update_item),
    url(r'^/cancel/(?P<id>\d+)$', views.cancel_trip),
    url(r'^/join/(?P<id>\d+)$', views.join_trip),
    url(r'^/delete/(?P<id>\d+)$', views.delete_item),
    url(r'^/logout$', views.logout),
    # url(r'^post_message', views.post_message),
]