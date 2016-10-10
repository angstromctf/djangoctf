from django.db import models


class Module(models.Model):
    # Textual information associated with module
    name = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=128)
    text = models.TextField()

    # Relationships with other modules
    prereqs = models.ManyToManyField('self', blank=True, related_name="required_for", symmetrical=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children", on_delete=models.CASCADE)
    first_child = models.ForeignKey('self', blank=True, null=True, related_name="first_parents", on_delete=models.SET_NULL)
    next = models.ForeignKey('self', blank=True, null=True, related_name="prevs", on_delete=models.SET_NULL)

    def __str__(self):
        return "Module[" + self.name + "]"
