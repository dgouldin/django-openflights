# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class BaseManager(models.Manager):
    def instance_is_dirty(self, instance, data, overwrite=False):
        """
        Returns ``True`` if the instance has attributes that are different
        from the values given in the data. Returns ``False`` otherwise.

        If ``overwrite`` is ``True``, the attributes of the instance are
        overwritten by the values given in the data.
        """
        dirty = False

        for k, v in data.items():
            if hasattr(instance, k) and getattr(instance, k) != v:
                dirty = True

                # Exit early if values are not being overwritten. Its
                # already known that the instance is dirty.
                if overwrite:
                    setattr(instance, k, v)
                else:
                    break

        return dirty

    def update_or_create(self, instance=None, force_save=True, **kwargs):
        if instance:
            created = False
        else:
            instance, created = self.get_or_create(**kwargs)
        if not created and 'defaults' in kwargs:
            dirty = self.instance_is_dirty(instance, kwargs['defaults'], True)
            if force_save or dirty:
                instance.save()
        return instance, created
