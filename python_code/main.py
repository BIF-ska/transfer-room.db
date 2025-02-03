#%%
from example_functions import say_bye, say_hi, say_hi_and_bye, return_a_dog
#%%

greeting = say_hi("Jørgen")

#%%

greeting = greeting.lower()

print(greeting)
#%%
# return a dog
dog = return_a_dog("Fido")

bark = dog.bark()

# variable for dog toys
toys = dog.favorite_toys

toy1 = toys[0]

#%%

new_toys: list = ["rope", "stick"]

dog.favorite_toys = new_toys
# %%

print(dog.favorite_toys)
# %%
