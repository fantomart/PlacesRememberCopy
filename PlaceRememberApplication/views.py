from django.shortcuts import render, redirect
from django.views import generic
from .models import Remember
from .forms import RememberForm
from PlacesRemember.settings import GOOGLE_MAPS_API_KEY

def home(request):
    if request.user.is_authenticated:
        return redirect('remember-list')
    else:
        return render(request, 'PlaceRememberApplication/about.html')


class RememberListView(generic.ListView):

    model = Remember
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
           return redirect("/")
        return super(RememberListView, self).get(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(RememberListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset


class RememberDetailView(generic.DetailView):
    model = Remember

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['lat'] = self.object.latitude
        context['lng'] = self.object.longitude
        context['GOOGLE_MAPS_API_KEY'] = GOOGLE_MAPS_API_KEY

        return context

    def get_queryset(self):
        queryset = super(RememberDetailView, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
           return redirect("/")
        return super(RememberDetailView, self).get(self, request, *args, **kwargs)

def remember_create(request):

    if (not request.user.is_authenticated):
        return redirect('/')

    remember_form = RememberForm(initial={"lat":"56.03580806601596", "lng":"92.91617590142528", "operation":"create",'GOOGLE_MAPS_API_KEY':GOOGLE_MAPS_API_KEY})
    if request.method == 'POST':

        remember_form = RememberForm(request.POST, request.FILES)

        print(request.POST)

        if remember_form.is_valid():
            new_remember = Remember.objects.create(**remember_form.cleaned_data)

            new_remember.user = request.user
            new_remember.latitude = request.POST['lat']
            new_remember.longitude = request.POST['lng']

            new_remember.save()

            return redirect('remember-list')

    return render(request, 'PlaceRememberApplication/remember_edit.html', {'remember_form': remember_form})


def remember_edit(request, pk):

    if (not request.user.is_authenticated):
        return redirect('/')

    inst = Remember.objects.get(id = pk)

    if (request.user != inst.user):
        return redirect('remember-list')

    remember_form = RememberForm(instance= inst, initial={"lat":inst.latitude, "lng":inst.longitude, "operation":"edit",'GOOGLE_MAPS_API_KEY':GOOGLE_MAPS_API_KEY})
    if request.method == 'POST':
        remember_form = RememberForm(request.POST, request.FILES, instance= Remember.objects.get(id = pk))

        if remember_form.is_valid():

            remember = remember_form.save()

            edited_remember = Remember.objects.get(id = pk)

            edited_remember.latitude = request.POST['lat']
            edited_remember.longitude = request.POST['lng']

            edited_remember.save()

            return redirect('remember-list')

    return render(request, 'PlaceRememberApplication/remember_edit.html', {'remember_form': remember_form})


