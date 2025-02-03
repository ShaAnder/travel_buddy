"""
Serializers for the Recommendations app.

This module contains the serializers used to convert model instances into
Python data types and vice versa for the `Recommendation` and `Category` models.
These serializers allow the data to be easily rendered into JSON for use in API responses.
"""
from rest_framework import serializers
from .models import *


class RecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recommendation model.

    This serializer is used to convert `Recommendation` model instances into
    JSON format, and vice versa, for use in API responses and requests.
    The serializer includes the recommendation's id, latitude, longitude, title,
    description, and address fields.

    Fields:
        id (int): The unique identifier of the recommendation.
        latitude (float): The latitude of the recommendation location.
        longitude (float): The longitude of the recommendation location.
        title (str): The title of the recommendation.
        description (str): A description of the recommendation.
        address (str): The address related to the recommendation.
    """

    class Meta:
        """
        Meta class for the RecommendationSerializer.

        This class defines the model (`Recommendation`) that the serializer is
        associated with and the fields that should be included in the serialized
        output. The `fields` list defines which model fields will be converted
        to JSON format.

        Attributes:
            model (Recommendation): The model associated with the serializer.
            fields (list): The list of fields to be included in the serialized data.
        """

        model = Recommendation
        fields = ['id', 'latitude', 'longitude', 'title', 'description', 'address']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer is used to convert `Category` model instances into
    JSON format, and vice versa, for use in API responses and requests.
    The serializer includes the category's id and name fields.

    Fields:
        id (int): The unique identifier of the category.
        name (str): The name of the category.
    """

    class Meta:
        """
        Meta class for the CategorySerializer.

        This class defines the model (`Category`) that the serializer is
        associated with and the fields that should be included in the serialized
        output. The `fields` list defines which model fields will be converted
        to JSON format.

        Attributes:
            model (Category): The model associated with the serializer.
            fields (list): The list of fields to be included in the serialized data.
        """
        
        model = Category
        fields = ['id', 'name']
