import csv
import os
import django

# Set the settings module (adjust path if needed)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sunren_site.settings')

# Initialize Django
django.setup()

from chemicals.models import Chemical, ChemicalGroup

with open('RawProductList.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(reader.fieldnames)
        print(row)
        # Clean column names to handle issues like BOM and extra spaces
        group_name = row['Group'].strip()
        cas_number = row['CAS# '].strip()  # Note the space after CAS#
        hs_code = row['H.S. Code'].strip()
        uses = row['Uses'].strip()
        product_name = row['Product'].strip()  # Handle BOM

        # Create or get group
        group, created = ChemicalGroup.objects.get_or_create(name=group_name)

        # Create Chemical object
        Chemical.objects.create(
            name=product_name,
            cas_number=cas_number,
            hs_code=hs_code,
            uses=uses,
            group=group
        )
