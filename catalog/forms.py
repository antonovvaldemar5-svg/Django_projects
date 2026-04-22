from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductForm(forms.ModelForm):
     FORBIDEN_WORDS = [
         "казино", "криптовалюта", "крипта",
         "биржа", "дешево", "бесплатно", "обман",
         "полиция", "радар"
     ]

     class Meta:
         model = Product
         fields = ["name", "description", "price"]


         def clean_name(self):
             name = self.cleaned_data.get('name')
             name_lower = name.lower()
             for word in self.FOFBIDEN_WORDS:
                 if word in name_lower:
                     raise forms.ValidationError(f"Название содержит запрещенное слово {word}")
             return name


         def clean_description(self):
             description = self.cleaned_data.get("description")
             description_lower = description.lower()
             for word in self.FORBIDEN_WORDS:
                 if word in description_lower:
                     raise forms.ValidationError(f"Описание содержит запрещенное слово {word}")
             return description


         def clean_price(self):
             price = self.cleaned_data.get("price")
             if price is None:
                 raise forms.ValidationError("Цена не указана")
             if price < 0:
                 raise forms.ValidationError("Цена не может быть отрицательной")
             return price


         def __init__(self, *args, **kwargs):
             super().__init__(*args, **kwargs)
             for field_name, field in self.fields.items():
                 field.widget.attrs['class'] = ('form_control')

                 if field_name == "name":
                     field.widget.attrs["placeholder"] = "Введите название товара"
                 elif field_name == "description":
                      field.widget.attrs["placeholder"] = "Введите описание товара"
                      field.widget.attrs ["rows"] = 5
                 elif field_name == "price":
                      field.widget.attrs["placeholder"] = "0.00"
                      field.widget.attrs["step"] = "0.01"





