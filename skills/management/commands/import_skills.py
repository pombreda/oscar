import csv
from django.core.management.base import BaseCommand

from skills.models import Skill


class Command(BaseCommand):
    args = '<csv file>'
    help = 'Import skills tree out of a csv file'

    def handle(self, *args, **options):
        dependancies = {}
        rubrique = ''

        for row in csv.DictReader(open(args[0], "r"), delimiter=",", quotechar='"'):

            rubrique = row['Rubrique'] if row['Rubrique'] else rubrique

            if Skill.objects.filter(code=row["Code"]).exists():
                skill = Skill.objects.get(code=row["Code"])
                skill.depends_on.clear()
                print "update", row["Code"]
            else:
                skill = Skill()
                print "create", row["Code"]
                skill.code = row["Code"]

            skill.name=row['Intitul\xc3\xa9']
            skill.description=row['Commentaires']
            skill.stage=row['\xc3\x89tape']
            skill.level=row['Niveau']
            skill.section=rubrique

            skill.save()

            for next_ in filter(lambda x: x, {row["suivant1"], row["suivant2"], row["suivant3"]}):
                dependancies.setdefault(row["Code"], []).append(next_)

        for key, value in filter(lambda (x, y): y, dependancies.iteritems()):
            print "on", key
            skill = Skill.objects.get(code=key)
            for dep in value:
                print " *", dep, "->", key
                Skill.objects.get(code=dep).depends_on.add(skill)
