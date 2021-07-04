import random
import string

from django.utils.timesince import timesince


def datetime_to_string(datetime):
    """
    Take a datetime object and return a nicely formatted string, eg: Aug 06, 2020 at 07:21 PM. 
    """
    return datetime.strftime("%b %d, %Y at %I:%M %p")

def rounded_timesince(datetime):
    """
    Take a datetime object and return the time between d and now rounded to lowest integer 
    as a nicely formatted string, eg: 7 hours, 16 minutes will be rounded to be 7 hours.
    """
    return timesince(datetime).split(",")[0]

def random_string_generator(length=10):
    """
    Generate a random alphanumeric string of letters and digits of a given fixed length.
    """
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def unique_slug_generator(instance, new_slug=None):
    """
    Generate a unique slug of given instance.
    """
    # check if the given arguments have a value of new slug
    # if yes, assign the given value to the slug field. 
    if new_slug is not None:
        slug = new_slug
    # if not, generate a slug of a random string.
    else:
        slug = random_string_generator()
    # get the instance class. 
    Klass = instance.__class__
    # check if there's any item with the same slug.
    qs_exists = Klass.objects.filter(slug=slug).exists()
    # if yes, generate a new slug of a random string and return recursive function with the new slug.
    if qs_exists:
        new_slug = random_string_generator()
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
