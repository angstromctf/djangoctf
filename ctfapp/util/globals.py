import datetime

contest = type("reference", (), {})
contest.start = datetime.datetime(2016, 2, 13, 0)
contest.end = datetime.datetime(2016, 2, 20, 0)

GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Non-binary')
)

RACE_CHOICES = (
    (1, 'American Indian or Alaskan Native'),
    (2, 'Asian'),
    (3, 'Black or African American'),
    (4, 'Native Hawaiian or Other Pacific Islander'),
    (5, 'White'),
    (6, 'Two or more races'),
    (7, 'Other'))