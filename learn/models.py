from django.db import models


class Module(models.Model):
    # Textual information associated with module
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    text = models.TextField()

    # Relationships with other modules
    prereqs = models.ManyToManyField('self', blank=True, related_name="required_for")
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children")
    first_child = models.ForeignKey('self', blank=True, null=True, related_name="parents")
    next = models.ForeignKey('self', blank=True, null=True, related_name="prevs")

    def __str__(self):
        return "Module[" + self.name + "]"