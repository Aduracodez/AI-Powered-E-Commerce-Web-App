from django.core.management.base import BaseCommand
from api.models import Product
import re


class Command(BaseCommand):
    help = 'Update product image URLs with proper Unsplash parameters'

    def handle(self, *args, **options):
        products = Product.objects.all()
        updated = 0
        
        for product in products:
            if product.image_url and 'unsplash.com' in product.image_url:
                original_url = product.image_url
                # Remove any trailing backslashes
                product.image_url = product.image_url.rstrip('\\')
                
                # Remove &fit=crop if present (causes 404 errors)
                if '&fit=crop' in product.image_url:
                    product.image_url = product.image_url.replace('&fit=crop', '')
                    product.image_url = product.image_url.replace('?fit=crop', '')
                    updated += 1
                
                # Ensure auto=format is present (without fit=crop)
                if 'auto=format' not in product.image_url and 'fit=crop' not in product.image_url:
                    if '?' in product.image_url:
                        product.image_url = product.image_url + '&auto=format'
                    else:
                        product.image_url = product.image_url + '?auto=format'
                    updated += 1
                
                if product.image_url != original_url:
                    product.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated} product image URLs')
        )

