from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

urlpatterns = [
    path('', never_cache(views.HomeList.as_view())),
    path('add-member', views.add_member, name='add'),
    path('edit-member/<str:member_id>', views.edit_member, name='edit_member')]
