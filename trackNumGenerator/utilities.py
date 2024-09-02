import random
import string
from trackNumGenerator.models import TrackingNumber

def generate_unique_tracking_number(length=16):
    """Generate a unique tracking number with a given length."""
    characters = string.ascii_uppercase + string.digits
    while True:
        tracking_number = ''.join(random.choices(characters, k=length))
        if not TrackingNumber.objects.filter(number=tracking_number).exists():
            return tracking_number