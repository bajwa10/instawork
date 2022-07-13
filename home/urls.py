from django.urls import path
from django.views.decorators.cache import never_cache
from .views import HomeList, AddMemberView, EditMemberView

urlpatterns = [
    path('', never_cache(HomeList.as_view())),
    path('add-member', AddMemberView.as_view(), name='add-member'),
    path('edit-member/<int:pk>', never_cache(EditMemberView.as_view()), name='edit-member')]
