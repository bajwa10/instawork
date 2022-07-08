from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.decorators.cache import never_cache
from dataclasses import dataclass
from .forms import MemberForm
from .models import Member


@dataclass
class OperationsHTML:
    heading: str
    sub_heading: str
    button_name: str
    is_edit: bool = False
    is_add: bool = False


class HomeList(ListView):
    model = Member
    template_name = "home.html"


def add_member(request):
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    spec = OperationsHTML(button_name='Add', heading='Add a team member', sub_heading='Set name, contact info and role',
                          is_add=True)
    context = {'form': form, 'spec': spec}
    return render(request, 'operations.html', context)


@never_cache
def edit_member(request, member_id):
    if not Member.objects.filter(pk=member_id):
        return redirect('/')
    member = Member.objects.get(pk=member_id)
    if 'delete' in request.POST:
        member.delete()
        return redirect('/')
    form = MemberForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        return redirect('/')
    spec = OperationsHTML(button_name='Edit', heading='Edit team member', sub_heading='Edit name, contact info and role'
                          , is_edit=True)
    context = {'form': form, 'spec': spec}
    return render(request, 'operations.html', context)
