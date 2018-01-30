# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# import ini dibutuhkan untuk IntegerField validator
from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.exceptions import ValidationError

class UserRate(models.Model):
    user = models.ForeignKey(User)
    place = models.ForeignKey("place.Place")
    rate_star = models.IntegerField(validators=[MaxValueValidator(5),
                                                MinValueValidator(0)])
    rate_comment = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.user.username
    
    # Methode clean() di overide untuk memberikan kemudahan validasi data
    # sebelum object disimpan
    def clean(self):
        if not self.place.is_active:
            raise ValidationError("User can't rate unactive place !")
        super(UserRate, self).clean()
    
    # class meta pada model digunakan untuk memberikan opsi unique_together
    # opsi ini akan memastikan bahwa tidak ada user yang memberikan rate
    # lebih dari satu kali pada Place yang sama.
    class Meta :
        unique_together = (("user", "place"),)
        
    # Methode ini dioveride agar kita dapat menampilan error message
    # yang sesuai keinginan kita saat melakukan validasi unique_together
    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('user', 'place'):
            return 'Oops, sorry duplicate rate !'
        else:
            return super(UserRate, self).unique_error_message(model_class, unique_check)