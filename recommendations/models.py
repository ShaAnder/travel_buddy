"""
Models for managing recommendations, categories, comments, and votes.

This module defines four key models used in the recommendations app:
- `Category`: Stores categories for recommendations.
- `Recommendation`: Represents recommendations made by users,
with associated details and a system for calculating votes.
- `Comment`: Allows users to comment on recommendations.
- `Vote`: Tracks user votes (upvote or downvote) for recommendations.

Each model includes essential fields and relationships for
handling the application's functionality.
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """
    Category model for organizing recommendations.

    Args:
        name (str): The name of the category.

    Description:
        This model is used to categorize recommendations.
        Each recommendation can belong to multiple categories.
        Categories are stored with unique names.
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        Return the string representation of the category.

        Returns:
            str: The category name.
        """
        return self.name


class Recommendation(models.Model):
    """
    Recommendation model representing user-submitted recommendations.

    Args:
        title (str): The title of the recommendation.
        user (ForeignKey): The user who created the recommendation.
        description (str, optional): A description of the recommendation.
        latitude (float, optional): Latitude for location-based recommendations.
        longitude (float, optional): Longitude for location-based recommendations.
        address (str): The address related to the recommendation.
        categories (ManyToManyField): Categories associated with the recommendation.

    Description:
        This model represents a recommendation that a user makes.
        It includes the title, description, address, and the location
        (latitude and longitude) of the recommendation. Multiple categories
        can be assigned to each recommendation, and the average
        vote score is calculated based on user feedback.
    """

    title = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )
    description = models.TextField(max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=255, unique=True)
    categories = models.ManyToManyField(
        Category,
        related_name="recommendations",
        blank=True,
    )

    def __str__(self):
        """
        Return a string representation of the recommendation.

        Returns:
            str: A formatted string including the recommendation
            title and user.
        """
        return f"{self.title} | Recommended by {self.user}"

    def average_score(self):
        """
        Calculate the average score based on user votes.

        Args:
            self (Recommendation): The recommendation instance.

        Description:
            This method tallies the votes associated with the
            recommendation and calculates the average score,
            rounding the result to one decimal place.
            If there are no votes, the function returns 0.

        Returns:
            float: The average vote score, rounded to one decimal place.
        """
        votes = self.votes.all()
        if votes.count() == 0:
            return 0
        total_score = sum(vote.vote for vote in votes)
        return round(total_score / votes.count(), 1)

    def delete_url(self):
        """
        Return the URL for deleting this recommendation.

        Returns:
            str: The URL for the delete recommendation view.
        """
        return reverse("delete_recommendation", args=[self.id])


class Comment(models.Model):
    """
    Comment model representing user comments on recommendations.

    Args:
        recommendation (ForeignKey): The recommendation being commented on.
        user (ForeignKey): The user who created the comment.
        body (str): The content of the comment.
        approved (bool): The approval status of the comment.
        created_on (DateTimeField): The date and time when the comment was created.

    Description:
        This model allows users to comment on recommendations.
        Comments are tracked with approval statuses and sorted by creation date.
    """

    class Meta:
        """
        Categorize the ordering that the model will use
        """
        ordering = ["created_on"]

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
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the comment.

        Returns:
            str: The comment by the user on the recommendation.
        """
        return f"Comment by {self.user} on {self.recommendation}"


class Vote(models.Model):
    """
    Vote model representing user votes on recommendations.

    Args:
        recommendation (ForeignKey): The recommendation being voted on.
        user (ForeignKey): The user who cast the vote.
        vote (IntegerField): The type of vote (1 for upvote, -1 for downvote).

    Description:
        This model tracks votes for each recommendation,
        allowing users to either upvote or downvote.
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
    vote = models.IntegerField(choices=VOTE_CHOICES)
    
    def __str__(self):
        """
        Return a string representation of the vote.

        Returns:
            str: A string indicating the vote value.
        """
        return f"{self.user} voted {self.get_vote_display()} on {self.recommendation}"
