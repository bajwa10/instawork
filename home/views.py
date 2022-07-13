from django.views.generic import ListView
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from .models import Member, MemberForm

template_name = "operations.html"


class HomeList(ListView):
    model = Member
    template_name = "home.html"


class AddMemberView(CreateView):
    model = Member
    template_name = template_name
    extra_context = {'operation': 'Add'}
    form_class = MemberForm
    success_url = '/'


class EditMemberView(UpdateView):
    model = Member
    template_name = template_name
    extra_context = {'operation': 'Edit'}
    form_class = MemberForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if not Member.objects.filter(pk=self.kwargs.get('pk')):
            return redirect('/')
        return super(EditMemberView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            Member.objects.get(pk=self.kwargs.get('pk')).delete()
            return redirect('/')
        return super().post(request, *args, **kwargs)
