from django.shortcuts import render

def profile(request):
    # user = request.User
    # # Access the profile via the `related_name`
    # profile = user.profile 
    # # Get all recommendations made by the user
    # recommendations = user.recommendations.all()  

    return render(request, "profiles/profile.html", {'show_navbar': True})
    # return render(request, "profiles/profile.html", {
    #     "profile": profile,
    #     "recommendations": recommendations,
    # })

