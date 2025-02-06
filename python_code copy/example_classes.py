class Dog:
    """
    A class to represent a dog
    """

    def __init__(self, name):
        self.name = name
        self.favorite_toys = ["bone", "ball", "frisbee"]

    def bark(self) -> str:

        """
        This function makes the dog bark
        """

        return(f"{self.name} says Woof!")

    def wag_tail(self) :
        """
        This function makes the dog wag its tail
        """
        return(f"{self.name} wags tail")

    def fetch(self):
        """
        This function makes the dog fetch
        """
        print(f"{self.name} fetches")

        print(f"{self.name} plays dead")

    def __str__(self):
        return self.name + " is a dog"