import pycountry

# Hent alle lande
countries = list(pycountry.countries)

# Udskriv antallet af lande
print(f"Antal lande i pycountry: {len(countries)}")
