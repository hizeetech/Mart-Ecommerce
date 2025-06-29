# Generated by Django 5.2 on 2025-04-10 10:17

import django.utils.timezone
import django_ckeditor_5.fields
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('cart_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, default='category.jpg', null=True, upload_to='category_images')),
                ('slug', models.SlugField(unique=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Text')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('gallery_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=10, prefix='')),
            ],
            options={
                'verbose_name_plural': 'Gallery',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Processing', 'Processing'), ('Failed', 'Failed')], default='Processing', max_length=100)),
                ('payment_method', models.CharField(blank=True, choices=[('PayPal', 'PayPal'), ('Stripe', 'Stripe'), ('Flutterwave', 'Flutterwave'), ('Paystack', 'Paystack'), ('RazorPay', 'RazorPay'), ('Monnify', 'Monnify')], default=None, max_length=100, null=True)),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100)),
                ('initial_total', models.DecimalField(decimal_places=2, default=0.0, help_text='The original total before discounts', max_digits=12)),
                ('saved', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Amount saved by customer', max_digits=12, null=True)),
                ('order_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=25, prefix='')),
                ('payment_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Order',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100)),
                ('shipping_service', models.CharField(blank=True, choices=[('DHL', 'DHL'), ('FedX', 'FedX'), ('UPS', 'UPS'), ('GIG Logistics', 'GIG Logistics')], default=None, max_length=100, null=True)),
                ('tracking_id', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('qty', models.IntegerField(default=0)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('initial_total', models.DecimalField(decimal_places=2, default=0.0, help_text='Grand Total of all amount listed above before discount', max_digits=12)),
                ('saved', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Amount saved by customer', max_digits=12, null=True)),
                ('applied_coupon', models.BooleanField(default=False)),
                ('item_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=25, prefix='')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(help_text='Display title for product', max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Sale Price')),
                ('regular_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Regular Price')),
                ('shipping', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Shipping Amount')),
                ('stock', models.PositiveIntegerField(default=0)),
                ('sku', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=5, max_length=50, prefix='SKU', unique=True)),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Disabled', 'Disabled')], default='Published', max_length=50)),
                ('featured', models.BooleanField(default=False, verbose_name='Marketplace Featured')),
                ('active', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Products',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('reply', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=None)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Variant Name')),
            ],
        ),
        migrations.CreateModel(
            name='VariantItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Item Title')),
                ('content', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Item Content')),
            ],
        ),
    ]
