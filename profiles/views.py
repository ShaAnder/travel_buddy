from django.shortcuts import render
from .models import Profile
from recommendations.models import Recommendation

# our profile view, we also import recommendations so the user can
# view all the recommendations they have made 
# (we want them to have CRUD control)
def profile_view(request):
    # acquire our user
    user = request.user
    # get the related profile tied to it
    profile = user.profile  
    # get all recommendations made by the user
    recommendations = user.recommendations.all() 

    # return the render of our profile, with the profile details and the 
    # recommonedations passed in
    return render(request, "profiles/profile.html", {
        "profile": profile,
        "recommendations": recommendations,
    })
