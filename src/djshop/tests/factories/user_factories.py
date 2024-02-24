from typing import Dict

from factory import PostGenerationMethodCall, Sequence
from factory.django import DjangoModelFactory

from src.djshop.users.models import BaseUser


class BaseUserFactory(DjangoModelFactory):

    """
    Factory class for creating instances of the BaseUser model.

    This factory provides a convenient way to generate
    test data for the BaseUser model in Django.
    It automatically generates unique email addresses,
    usernames, and sets a default password for each
    created instance.
    """

    class Meta:
        model = BaseUser

    email = Sequence(
        lambda instance_num: f'test_user_{instance_num}@example.com'
    )

    username = Sequence(
        lambda instance_num: f'test_user_{instance_num}'
    )

    password = PostGenerationMethodCall(
        'set_password', 'test_pass0'
    )

    @classmethod
    def create_payload(cls) -> Dict[str, str]:

        """
        A class method that generates a payload dictionary for creating
        a user via the API.
        :return: generate a payload dictionary with consistent values
        for creating users via the API.
        """

        test_user = cls.build()
        return {
            'email': str(test_user.email),
            'username': str(test_user.username),
            'password': 'test_pass0',
            'confirm_password': 'test_pass0',
        }

    @classmethod
    def create_superuser(cls) -> 'BaseUser':

        """
        A class method that creates a superuser instance.

        :return: The newly created superuser instance.
        """

        test_user = cls.build()

        superuser = BaseUser.objects.create_superuser(
            email=str(test_user.email),
            username=str(test_user.username),
            password='test_pass0',
        )
        return superuser

    # @factory.post_generation
    # def profile(self, create: bool, extracted: Optional['Profile'], **kwargs):
    #
    #     """
    #     Post-generation hook to create a related Profile instance for the BaseUser.
    #
    #     :param create: (bool): Flag indicating whether to create a related Profile.
    #     :param extracted: A Profile instance that can be passed in.
    #     :param kwargs:
    #     :return:
    #     """
    #
    #     if not create:
    #         # Simple build, do nothing.
    #         return
    #
    #     if extracted:
    #         # A profile was passed in, use it
    #         self.profile = extracted
    #     else:
    #         # No profile was passed in, create one
    #         ProfileFactory(user=self)
