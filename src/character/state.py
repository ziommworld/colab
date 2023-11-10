class State:
    def __init__(self, name, duration, intensity=1):
        self.name = name
        self.duration = duration  # Use -1 for indefinite duration, otherwise specify the number of rounds
        self.intensity = intensity  # The intensity or magnitude of the state's effects

    def increase_intensity(self, amount=1):
        """
        Increment the intensity of the state by a given amount.
        We don't need decrease, as we reeavulate each time.
        """
        self.intensity += amount
        
    def increase_duration(self, amount=1):
        """
        Increment the intensity of the state by a given amount.
        We don't need decrease, as we reeavulate each time.
        """
        self.intensity += amount

    def decrement_duration(self):
        """
        Decrement the duration of the state by one round, unless it's indefinite.
        """
        if self.duration > 0:
            self.duration -= 1

    def is_expired(self):
        """
        Check if the state's duration has expired, indicating it should be removed.
        """
        return self.duration == 0
