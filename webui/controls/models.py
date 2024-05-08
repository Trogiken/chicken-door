from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import pytz


class SystemConfig(models.Model):
    # time zone choice class
    board_mode = models.CharField(max_length=5, choices=[("BCM", "BCM"), ("BOARD", "BOARD")], default=("BCM", "BCM"), verbose_name="Board Mode", help_text="GPIO pin numbering mode")
    relay1 = models.IntegerField(default=26, validators=[MinValueValidator(1), MaxValueValidator(40)], verbose_name="Relay 1", help_text="Extending Motion")
    relay2 = models.IntegerField(default=20, validators=[MinValueValidator(1), MaxValueValidator(40)], verbose_name="Relay 2", help_text="Retraction Motion")
    switch1 = models.IntegerField(default=6, validators=[MinValueValidator(1), MaxValueValidator(40)], verbose_name="Switch 1", help_text="Extend Limit")
    switch2 = models.IntegerField(default=13, validators=[MinValueValidator(1), MaxValueValidator(40)], verbose_name="Switch 2", help_text="Retract Limit")
    switch3 = models.IntegerField(default=19, validators=[MinValueValidator(1), MaxValueValidator(40)], verbose_name="Switch 3", help_text="Door path is blocked")
    switch4 = models.IntegerField(default=23, validators=[MinValueValidator(1), MaxValueValidator(40)], verbose_name="Switch 4", help_text="Aux switch for 'Relay 1'")
    switch5 = models.IntegerField(default=24, validators=[MinValueValidator(1), MaxValueValidator(40)], verbose_name="Switch 5", help_text="Aux switch for 'Relay 2'")
    off_state = models.BooleanField(choices=[(True, "On"), (False, "Off")], default=True, verbose_name="Off State", help_text="Power setting for relay off state")
    timezone = models.CharField(max_length=100, choices=[(tz, tz) for tz in pytz.all_timezones], verbose_name="Timezone", help_text="Timezone of hardware")
    longitude = models.DecimalField(default=0.0, max_digits=9, decimal_places=6, verbose_name="Longitude", help_text="Longitudinal location of hardware")
    latitude = models.DecimalField(default=0.0, max_digits=9, decimal_places=6, verbose_name="Latitude", help_text="Latitudinal location of hardware")
    travel_time = models.IntegerField(default=10, verbose_name="Travel Time", help_text="Allowed time, in seconds, for the door to be in motion")

    def __str__(self):
        return "SystemConfig"

    def save(self, *args, **kwargs):
        if not self.pk and SystemConfig.objects.exists():
            raise PermissionError('There can only be 1 SystemConfig instance')
        return super(SystemConfig, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "System Config"
        verbose_name_plural = "System Configs"


class StartupConfig(models.Model):
    # property function to give sunrise and sunset time?

    automation = models.BooleanField(default=False, verbose_name="Automation", help_text="Toggle automation on or off")
    auxiliary = models.BooleanField(default=False, verbose_name="Auxiliary", help_text="Toggle auxiliary on or off")
    sunrise_offset = models.IntegerField(default=0, verbose_name="Sunrise Offset", help_text="Add or subtract minutes from sunrise")
    sunset_offset = models.IntegerField(default=0, verbose_name="Sunset Offset", help_text="Add or subtract minutes from sunset")

    def __str__(self):
        return "StartupConfig"

    def save(self, *args, **kwargs):
        if not self.pk and StartupConfig.objects.exists():
            raise PermissionError('There can only be 1 StartupConfig instance')
        return super(StartupConfig, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Startup Config"
        verbose_name_plural = "Startup Configs"