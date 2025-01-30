from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

### MODELS ###

class Category(models.Model):
    """Category model

    Args:
        models (django model class): class from djangos model framework

    Description:
        category model for the recommendations, a many to many relationship and we will
        populate these ourself, we take this route to allow the user to select multiple
        categories for each recommendation.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Recommendation(models.Model):
    """Recommendation model

    Args:
        models (django model class): class from djangos model framework

    Description:
        recommendation model for the database, once created here get's migrated
        to the database and is used for allowing users to see active recommendations 
        made
    """

    def __str__(self):
        """String func

        Returns:
            formatted string for admin viewing 
        """
        return f"{self.title} | Recommended by {self.user}"
    
    #title of the recommendation
    title = models.CharField(max_length=100, unique=True)
    # user, our fk linking back to the user who created it
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )
    # optional description field for the recommendation
    description = models.TextField(max_length=200, blank=True, null=True)
    # we add lat/long cords for rec to put on map (invisible to user)
    latitude = models.FloatField(blank=True, null=True)  
    longitude = models.FloatField(blank=True, null=True)
    # address of place in question
    address = models.CharField(max_length=255, unique=True)
    # Many-to-many field for categories
    categories = models.ManyToManyField(
        Category,
        related_name="recommendations",
        blank=True,
    )

    def average_score(self):
        """
        Average Score Func

        Args:
            self: (num): number to average

        Description:
            Method to calculate the votes, the votes are added by users and calculated here
            when the object (recommendation) is displayed, the vote is tallied and then shown
        """
        votes = self.votes.all()
        if votes.count() == 0:
            # No votes, return 0 as default
            return 0  
        total_score = sum(vote.vote for vote in votes)
        # Return the average score, rounded to 1 decimal place
        return round(total_score / votes.count(), 1)
    
    def delete_url(self):
        return reverse("delete_recommendation", args=[self.id])

class Comment(models.Model):
    """Comment model

    Args:
        models (django model class): class from djangos model framework

    Description:
        comment model for the users comments on each recommendation, allows 
        us to populate comments on the recommendation models we will create later
    """
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


class Vote(models.Model):
    """Vote model

    Args:
        models (django model class): class from djangos model framework

    Description:
        simple vote model to track if user has created a vote for a specific
        recommendation or not, we want to create a rating system for each
        recommendation.
    """
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]

    recommendation = models.ForeignKey(
        Recommendation,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    # The actual vote, either upvote (1) or downvote (-1)
    vote = models.IntegerField(choices=VOTE_CHOICES)

