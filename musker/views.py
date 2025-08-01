from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Meep, Community
from .forms import MeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Community, Comment
from .forms import CommentForm


def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None, request.FILES or None)  # Handle files here
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, "Your Message Has Been Posted!")
                return redirect('home')

        meeps = Meep.objects.all().order_by("-created_at")
        communities = Community.objects.all()  # Display all communities on the home page
        return render(request, 'home.html', {"meeps": meeps, "form": form, "communities": communities})
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        communities = Community.objects.all()
        return render(request, 'home.html', {"meeps": meeps, "communities": communities})



def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles":profiles})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

def unfollow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.remove(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

def follow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.add(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')




def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")

		# Post Form logic
		if request.method == "POST":
			# Get current user
			current_user_profile = request.user.profile
			# Get form data
			action = request.POST['follow']
			# Decide to follow or unfollow
			if action == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action == "follow":
				current_user_profile.follows.add(profile)
			# Save the profile
			current_user_profile.save()



		return render(request, "profile.html", {"profile":profile, "meeps":meeps})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')		

def followers(request, pk):
	if request.user.is_authenticated:
		if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			return render(request, 'followers.html', {"profiles":profiles})
		else:
			messages.success(request, ("That's Not Your Profile Page..."))
			return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')


def follows(request, pk):
	if request.user.is_authenticated:
		if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			return render(request, 'follows.html', {"profiles":profiles})
		else:
			messages.success(request, ("That's Not Your Profile Page..."))
			return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')



def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!  Get POSTING!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error logging in. Please Try Again..."))
			return redirect('login')

	else:
		return render(request, "login.html", {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You Have Been Logged Out. Sorry to See You Go..."))
	return redirect('home')

def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # This returns the User object
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Optional: If you have a Profile model linked via OneToOneField
            Profile.objects.create(user=user)  # ✅ user, not user.id

            # Authenticate and login
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')

    return render(request, "register.html", {'form': form})


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		# Get Forms
		user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			login(request, current_user)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
	
def meep_like(request, pk):
	if request.user.is_authenticated:
		meep = get_object_or_404(Meep, id=pk)
		if meep.likes.filter(id=request.user.id):
			meep.likes.remove(request.user)
		else:
			meep.likes.add(request.user)
		
		return redirect(request.META.get("HTTP_REFERER"))




	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')


def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.meep = meep
            comment.save()
            messages.success(request, "Your comment has been posted!")
            return redirect('meep_show', pk=meep.pk)
    else:
        form = CommentForm()

    return render(request, 'show_meep.html', {'meep': meep, 'form': form})


def delete_meep(request, pk):
	if request.user.is_authenticated:
		meep = get_object_or_404(Meep, id=pk)
		# Check to see if you own the meep
		if request.user.username == meep.user.username:
			# Delete The Meep
			meep.delete()
			
			messages.success(request, ("The Post Has Been Deleted!"))
			return redirect(request.META.get("HTTP_REFERER"))	
		else:
			messages.success(request, ("You Don't Own That Post!!"))
			return redirect('home')

	else:
		messages.success(request, ("Please Log In To Continue..."))
		return redirect(request.META.get("HTTP_REFERER"))


def edit_meep(request,pk):
	if request.user.is_authenticated:
		# Grab The Meep!
		meep = get_object_or_404(Meep, id=pk)

		# Check to see if you own the meep
		if request.user.username == meep.user.username:
			
			form = MeepForm(request.POST or None, instance=meep)
			if request.method == "POST":
				if form.is_valid():
					meep = form.save(commit=False)
					meep.user = request.user
					meep.save()
					messages.success(request, ("Your Post Has Been Updated!"))
					return redirect('home')
			else:
				return render(request, "edit_meep.html", {'form':form, 'meep':meep})
	
		else:
			messages.success(request, ("You Don't Own That Post!!"))
			return redirect('home')

	else:
		messages.success(request, ("Please Log In To Continue..."))
		return redirect('home')



def search(request):
	if request.method == "POST":
		# Grab the form field input
		search = request.POST['search']
		# Search the database
		searched = Meep.objects.filter(body__contains = search)

		return render(request, 'search.html', {'search':search, 'searched':searched})
	else:
		return render(request, 'search.html', {})
	
def join_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if request.user not in community.members.all():
        community.members.add(request.user)
        messages.success(request, f"You have successfully joined the '{community.name}' community!")
    else:
        messages.info(request, f"You are already a member of the '{community.name}' community.")
    return redirect('community_list')

def community_detail(request, pk):
    # Fetch the community based on the primary key (pk)
    community = get_object_or_404(Community, pk=pk)

    # Get all the posts (Meep) associated with the community
    meeps = Meep.objects.filter(community=community).order_by("-created_at")

    # Handle the creation of a new Meep post
    if request.method == "POST":
        if request.user in community.members.all():  # Ensure user is a member
            body = request.POST.get("body")
            if body:
                Meep.objects.create(
                    body=body,
                    user=request.user,
                    community=community
                )
                messages.success(request, "Your post has been created!")
                return redirect('community_detail', pk=community.pk)
            else:
                messages.error(request, "Post content cannot be empty.")
        else:
            messages.warning(request, "You must join the community to post.")
            return redirect('community_list')  # Redirect to community list if not a member

    return render(request, 'community_detail.html', {
        'community': community,
        'meeps': meeps
    })

def community_list(request):
    communities = Community.objects.all()
    return render(request, 'community_list.html', {"communities": communities})

# Create a new community
def create_community(request):
    if not request.user.is_authenticated:
        messages.success(request, "You Must Be Logged In To View This Page...")
        return redirect('home')

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        # ✅ First, save the Community so it gets an ID
        community = Community.objects.create(
            name=name,
            description=description,
            creator=request.user
        )

        # ✅ Then, safely add the creator as a member
        community.members.add(request.user)

        messages.success(request, f"Community '{name}' created and you've been added as a member!")
        return redirect('community_list')
    
    return render(request, 'create_community.html')


def unjoin_community(request, pk):
    community = get_object_or_404(Community, pk=pk)

    # 🚫 Prevent the creator from leaving their own community
    if request.user == community.creator:
        messages.error(request, f"You are the creator of '{community.name}' and cannot unjoin your own community.")
        return redirect('community_list')

    if request.user in community.members.all():
        community.members.remove(request.user)
        messages.success(request, f"You have successfully left the '{community.name}' community!")
    else:
        messages.warning(request, f"You are not a member of the '{community.name}' community.")

    return redirect('community_list')  # Redirect back to the community list page


def comment_on_meep(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.meep = meep
            comment.save()
            messages.success(request, "Your comment has been posted!")
            return redirect('meep_show', pk=meep.pk)
    else:
        form = CommentForm()
    return render(request, "comment_form.html", {'form': form, 'meep': meep})