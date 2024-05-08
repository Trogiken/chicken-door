# Generated by Django 4.2 on 2023-04-18 23:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controls', '0006_alter_startupconfig_options_startupconfig_auxillary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='startupconfig',
            options={'verbose_name': 'Startup Config', 'verbose_name_plural': 'Startup Configs'},
        ),
        migrations.AlterField(
            model_name='startupconfig',
            name='automation',
            field=models.BooleanField(default=False, help_text='Toggle automation on or off', verbose_name='Automation'),
        ),
        migrations.AlterField(
            model_name='startupconfig',
            name='auxillary',
            field=models.BooleanField(default=False, help_text='Toggle auxillary on or off', verbose_name='Auxillary'),
        ),
        migrations.AlterField(
            model_name='startupconfig',
            name='sunrise_offset',
            field=models.IntegerField(default=0, help_text='Add or subtract minutes from sunrise', verbose_name='Sunrise Offset'),
        ),
        migrations.AlterField(
            model_name='startupconfig',
            name='sunset_offset',
            field=models.IntegerField(default=0, help_text='Add or subtract minutes from sunset', verbose_name='Sunset Offset'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=0.0, help_text='This is the help text for latitude', max_digits=9, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=0.0, help_text='This is the help text for longitude', max_digits=9, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='off_state',
            field=models.CharField(choices=[('True', 'On'), ('False', 'Off')], default='True', help_text='This is the help text for off_state', max_length=5, verbose_name='Off State'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='relay1',
            field=models.IntegerField(default=26, help_text='This is the help text for relay1', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(31)], verbose_name='Relay 1'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='relay2',
            field=models.IntegerField(default=20, help_text='This is the help text for relay2', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(31)], verbose_name='Relay 2'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='switch1',
            field=models.IntegerField(default=6, help_text='This is the help text for switch1', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(31)], verbose_name='Switch 1'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='switch2',
            field=models.IntegerField(default=13, help_text='This is the help text for switch2', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(31)], verbose_name='Switch 2'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='switch3',
            field=models.IntegerField(default=19, help_text='This is the help text for switch3', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(31)], verbose_name='Switch 3'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='switch4',
            field=models.IntegerField(default=23, help_text='This is the help text for switch4', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(31)], verbose_name='Switch 4'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='switch5',
            field=models.IntegerField(default=24, help_text='This is the help text for switch5', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(31)], verbose_name='Switch 5'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='timezone',
            field=models.CharField(help_text='This is the help text for timezone', max_length=100, verbose_name='Timezone'),
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='travel_time',
            field=models.IntegerField(default=10, help_text='This is the help text for travel_time', verbose_name='Travel Time'),
        ),
    ]
