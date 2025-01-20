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
    description = models.TextField(max_length=200, blank=True, null=True)

### comment model




