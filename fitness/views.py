from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from fitness.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from fitness.models import Workout, Exercise
from fitness.forms import WorkoutForm, UserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


# Create your views here.

def index(request):
    workout_list = Workout.objects.order_by('-likes')[:3]
    return render(request, 'fitness/index.html', context={'workouts': workout_list})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Fitness fanatic account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'fitness/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def FAQ(request):
    # return HttpResponse("This is the FAQ page")
    return render(request, 'fitness/FAQ.html', context={})


def about(request):
    # return HttpResponse("This is the about us page <a href='/fitness_fanatics/'>Home</a>")
    return render(request, 'fitness/about.html', context={})


def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'fitness/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def view_workout(request, workout_name_slug):
    
    context_dict = {}
    try:
        workout = Workout.objects.get(slug=workout_name_slug)
        try:
            author = User.objects.get(id = workout.author)
            context_dict['author'] = author
        except:
            author = None
            
            
        is_liked = False
        if workout.likes.filter(id=request.user.id).exists():
            is_liked = True
        
        is_favourite = False
        if workout.favourite.filter(id=request.user.id).exists():
            print("is fav")
            is_favourite = True
            
        context_dict = {'author' : author,
                        'workout' : workout,
                        'is_liked' : is_liked,
                        'total_likes' : workout.total_likes(),
                        'is_favourite' : is_favourite,}
        
    except Workout.DoesNotExist:
        context_dict['workout'] = None
    return render(request, 'fitness/view_workout.html', context_dict)

def nearby_gyms(request):
    return render(request, 'fitness/nearby_gyms.html', {})

def all_workouts(request):
    workout_list = Workout.objects.order_by("-likes")
    page = request.GET.get('page', 1)

    paginator = Paginator(workout_list, 6)
    try:
        workouts = paginator.page(page)
    except PageNotAnInteger:
        workouts = paginator.page(1)
    except EmptyPage:
        workouts = paginator.page(paginator.num_pages)

    return render(request, 'fitness/workouts.html', context={"workouts": workouts})


@login_required
def my_workouts(request):
    workout_list = Workout.objects.filter(author = request.user.id)
    return render(request, 'fitness/my_workouts.html', context={'workouts': workout_list})

@login_required
def add_workout(request):
    form = WorkoutForm()

    if request.method == 'POST':
        form = WorkoutForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return index(request)
        else:
            print(form.errors)

    return render(request, 'fitness/add_workout.html', {'form': form})


@login_required
def add_exercise(request, workout_name_slug):

    try:
        workout = Workout.objects.get(slug=workout_name_slug)
    except Workout.DoesNotExist:
        workout = None

    form = ExerciseForm()
    if request.method == 'POST':
        form = ExerciseForm(reuqest.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.views = 0
            exercise.save()
            return show_workout(request, workout_name_slug)
        else:
            print(form.erros)

    context_dict = {'form': form, 'workout': workout}
    return render(request, 'fitness/add_exercise.html', context_dict)


@login_required
def my_account(request):
    return HttpResponse("This is the my account page")


def like_workout(request):
    workout = get_object_or_404(Workout, id=request.POST.get('workout_id'))
    is_liked = False
    
    if workout.likes.filter(id=request.user.id).exists():
        workout.likes.remove(request.user)
        is_liked = False
    else:
        workout.likes.add(request.user)
        is_liked = True 
    return HttpResponseRedirect(workout.get_absolute_url())

def favourite_workout(request):
    
    workout = get_object_or_404(Workout, id=request.POST.get('workout_id'))
    is_favourite = False

    if workout.favourite.filter(id=request.user.id).exists():
        print("unfavoured")
        workout.favourite.remove(request.user)
        is_favourite = False
    else:
        workout.favourite.add(request.user)
        print("favourited")
        is_favourite  = True
        
    return HttpResponseRedirect(workout.get_absolute_url())

@login_required
def favourites(request):

    workout_list = Workout.objects.filter(favourite = request.user.id)

    return render(request, 'fitness/favourites.html', context={'workouts': workout_list})


            
    











    


    






