from django.db import models


class Node(models.Model):
    prereq = models.ForeignKey('self', blank=True, null=True)

    name = models.CharField(max_length=100)

    def __str__(self):
        return "Node[" + self.name + "]"


class Category(Node):
    members = models.ManyToManyField(Node, related_name="categories_set")
    first_child = models.ForeignKey(Node, related_name="first_child_set")

    def __str__(self):
        return "Category[" + self.name + "]"


class Module(Node):
    text = models.TextField()

    def __str__(self):
        return "Module[" + self.name + "]"