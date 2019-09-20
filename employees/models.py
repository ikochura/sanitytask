# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User


@property
def full_name(self):
    return "{} {}".format(self.first_name, self.last_name)


User.add_to_class('full_name', full_name)
