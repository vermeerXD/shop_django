from django.db import models
from django.core.exceptions import ValidationError
from shop.models import Category, Product

# Create your models here.
class Smartphone(models.Model):
    """Model for Smartphone"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='smartphone')

    color = models.CharField(max_length=50, verbose_name="Колір")
    processor = models.CharField(max_length=100, verbose_name="Процесор")
    ram = models.PositiveIntegerField(verbose_name="Оперативна пам'ять (RAM) в ГБ")
    rom = models.PositiveIntegerField(verbose_name="Вбудована пам'ять (ROM) в ГБ")
    battery_capacity = models.PositiveIntegerField(verbose_name="Ємність батареї (мА·год)")
    screen_size = models.FloatField(verbose_name="Розмір екрану (дюйми)")
    hz_of_display = models.PositiveIntegerField(verbose_name="Частота диcплею", null=True, blank=True)
    camera_specifications = models.CharField(max_length=255, verbose_name="Характеристики камер",
                                             help_text="Наприклад: 108МП + 12МП + 5МП", null=True)
    operating_system = models.CharField(max_length=100, verbose_name="Операційна система", null=True, blank=True)
    display_type = models.CharField(max_length=100, verbose_name="Тип дисплея", help_text="Наприклад: AMOLED, IPS, LCD",
                                    null=True)
    supports_5g = models.BooleanField(default=False, verbose_name="Підтримка 5G")
    waterproof_rating = models.CharField(max_length=50, null=True, blank=True,
                                         verbose_name="Клас захисту (водостійкість)", help_text="Наприклад: IP68")
    weight = models.FloatField(null=True, blank=True, verbose_name="Вага (грам)")
    additional_features = models.TextField(null=True, blank=True, verbose_name="Додаткові функції",
                                           help_text="Наприклад: підтримка стилуса, безпровідна зарядка")
    brand = models.CharField(null=True, blank=True, verbose_name="Бренд", max_length=50)

    def clean(self):
        if self.product.category.id != 5:
            raise ValidationError("Продукт повинен належати до категорії 'Смартфони' (id=5).")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.color}, {self.ram}GB RAM, {self.rom}GB ROM"

class Case(models.Model):
    """Model for Case"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='case')

    material = models.CharField(max_length=100, verbose_name="Матеріал")
    compatible_models = models.TextField(verbose_name="Сумісні моделі")
    color = models.CharField(max_length=50, verbose_name="Колір")
    brand = models.CharField(max_length=50, verbose_name="Бренд", null=True, blank=True)

    def clean(self):
        if self.product.category.id != 2:
            raise ValidationError("Продукт повинен належати до категорії 'Чохли' (id=2).")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.material}, {self.color}"

class ScreenProtector(models.Model):
    """Model for Screen Protector"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='screen_protector')

    hardness_rating = models.CharField(max_length=20, verbose_name="Рейтинг твердості")
    anti_glare = models.BooleanField(default=False, verbose_name="Антиблікове покриття")
    compatible_models = models.TextField(verbose_name="Сумісні моделі")
    brand = models.CharField(max_length=50, verbose_name="Бренд", null=True, blank=True)

    def clean(self):
        if self.product.category.id != 3:
            raise ValidationError("Продукт повинен належати до категорії 'Захисне скло' (id=3).")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.hardness_rating}"

class PowerBank(models.Model):
    """Model for Power Bank"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='power_bank')

    capacity_mAh = models.PositiveIntegerField(verbose_name="Ємність батареї (мА·год)")
    type = models.TextField(verbose_name="Тип батареї", null=True)
    output_power_w = models.PositiveIntegerField(verbose_name="Потужність (Вт)")
    usb_ports = models.PositiveIntegerField(verbose_name="Кількість USB портів")
    supports_wireless_charging = models.BooleanField(default=False, verbose_name="Підтримка бездротової зарядки")
    brand = models.CharField(max_length=50, verbose_name="Бренд", null=True, blank=True)

    def clean(self):
        if self.product.category.id != 4:
            raise ValidationError("Продукт повинен належати до категорії 'Павербанки' (id=4).")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.capacity_mAh}mAh, {self.usb_ports} портів"

class CableAndAdapter(models.Model):
    """Model for Cable and Adapter"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='cable_adapter')

    cable_type = models.CharField(max_length=50, verbose_name="Тип кабелю")
    length_cm = models.PositiveIntegerField(verbose_name="Довжина кабелю (см)")
    connector_1 = models.TextField(verbose_name="Розʼєм 1", null=True)
    connector_2 = models.TextField(verbose_name="Розʼєм 2", null=True)
    brand = models.CharField(max_length=50, verbose_name="Бренд", null=True, blank=True)

    def clean(self):
        if self.product.category.id != 6:
            raise ValidationError("Продукт повинен належати до категорії 'Кабелі та перехідники' (id=6).")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.cable_type}, {self.length_cm}см"

class Charger(models.Model):
    """Model for Charger"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='charger')

    output_power_w = models.PositiveIntegerField(verbose_name="Потужність (Вт)")
    ports = models.PositiveIntegerField(verbose_name="Кількість портів")
    fast_charge = models.BooleanField(default=False, verbose_name="Швидка зарядка")
    brand = models.CharField(max_length=50, verbose_name="Бренд", null=True, blank=True)

    def clean(self):
        if self.product.category.id != 7:
            raise ValidationError("Продукт повинен належати до категорії 'Зарядні пристрої' (id=7).")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.output_power_w}Вт, {self.ports} портів"