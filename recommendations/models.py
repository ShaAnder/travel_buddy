from django.db import models
from django.contrib.auth.models import User

# Now we create our models:

### Recommendation model

class Recommendation(models.Model):
    # String representation for the places we create
    def __str__(self):
        return f"{self.title} | Recommended by {self.user}"
    
    # Our fields for the database
    # title field, our PK we want it unique to prevent duplicates
    title = models.CharField(max_length=100, unique=True)
    # user, our fk linking back to the user who created it
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )
    # description, optional field to add a short description about the place
    description = models.TextField(max_length=200, blank=True, null=True)
    # we add in our lat and long, these can be null initially but they are needed to pin
    # markers on the map we won't have users fill these in 
    latitude = models.FloatField(blank=True, null=True)  
    longitude = models.FloatField(blank=True, null=True)
    # then we will get the address
    address = models.CharField(max_length=255, unique=True)
    # finally a category for what the user wants to label it as,
    # will add a filtering option later to pull the correct 
    # categories a user filters
    category = models.CharField(max_length=50, blank=True, null=True)

    # OPTIONAL we will add a created on for auditing or debugging purposes
    created_on = models.DateTimeField(auto_now_add=True)

### comment model

class Comment(models.Model):
    # Metadata for ordering comments
    class Meta:
        ordering = ["created_on"] 
    def __str__(self):
        return f"Comment by {self.user} on {self.recommendation}"
    # foreign keys to backtrack to our recommendation and user
    recommendation = models.ForeignKey(
        Recommendation,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user_comments",
    )
    # comment content
    body = models.TextField()
    # bool for approved status, we will want the moderators to approve
    approved = models.BooleanField(default=False)
    # created on date for accurate judging
    created_on = models.DateTimeField(auto_now_add=True)
