from django.db import models

class Spell(models.Model):
    name = models.CharField(max_length=64,
        help_text='Complete spell name. Use proper capitalization, and put the '
                  'base name of the spell at the front, i.e. "Heal, Mass" '
                  'instead of "Mass Heal".')
    altname = models.SlugField(max_length=64,
        help_text='URL version of the name; use only alphanumeric char, dashes '
                  'and keep the text in lowercase except for roman numerals.')
    school = models.CharField(max_length=32,
        help_text='School of magic, for example "Illusion"') # Probably a FK to a list
    subschool = models.CharField(max_length=32, blank=True,
        help_text='Subschool of the magic school, if any. Example: "Figment"') # probably a FK to a list
    descriptor = models.CharField(max_length=64, blank=True,
        help_text='Descriptor list (comma separated). Example "Fire, Chaos"') # A Many to Many to a table. probably with an attribute (may have all of the descriptors or any of them)
    spellcraft_dc = models.CharField(max_length=64, blank=True,
        verbose_name='Spellcraft DC',
        help_text='DC to cast (epic spells)') # This should be a nullable int, possibly with a flag for see text notes
    level = models.CharField(max_length=128, blank=True,
        help_text='Comma separated list of Class lvl. Example: "Bard 3, Sor/Wiz 4"') # This should be a many-to-many to class level
    components = models.TextField(
        help_text='Comma separated list,as shown in spell. Example: "V, S, M/DF, XP"') # This should be a set of flags: V, S, M, F, DF, XP, ... possibly from the nullability of other fields
    casting_time = models.CharField(max_length=32) # amount + unit, sometimes with notes
    range = models.CharField(max_length=64) # Maybe normalized, but more complex
    target = models.CharField(max_length=256, blank=True)
    area = models.CharField(max_length=256, blank=True)
    effect = models.CharField(max_length=256, blank=True)
    duration = models.CharField(max_length=128)
    saving_throw = models.CharField(max_length=128) # may be normalized, not sure 
    spell_resistance = models.CharField(max_length=64) # may be normalized, not sure 
    short_description = models.CharField(max_length=128,
        help_text='Short description shown in spell lists')
    to_develop = models.TextField(blank=True,
        help_text='Cost to develop epic spell')
    material_components = models.TextField(blank=True)
    arcane_material_components = models.CharField(max_length=256, blank=True)
    focus = models.TextField(blank=True)
    description = models.TextField(blank=True)
    xp_cost = models.TextField(blank=True)
    arcane_focus = models.CharField(max_length=256, blank=True)
    verbal_components = models.CharField(max_length=256, blank=True) # only used in 1 spell. Possibly should meld into description
    cleric_focus = models.CharField(max_length=256, blank=True)
    druid_focus = models.CharField(max_length=256, blank=True)
    reference = models.CharField(max_length=30,
        help_text='Book containing the spell and pag. Example: "SpC 31"') # Should be a FK

    @models.permalink
    def get_absolute_url(self):
        return ('spell_detail', [], {'id': self.id})

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'spell'
        ordering = ('name',)


class Source(models.Model):
    name = models.CharField(max_length=128,
        help_text='Handbook or Manual name')
    altname = models.CharField(max_length=128,
        help_text='URL version of the name; use only alphanumeric char, dashes ')
    initials = models.CharField(max_length=30,
        help_text='Initials to show in feat and spell descriptions: ex "SpC, PHB"')

    def __unicode__(self):
        return self.initials


class FeatType(models.Model):
    name = models.CharField(max_length=30)
    altname = models.SlugField(max_length=30,
        help_text='URL version of the name; use only alphanumeric char, dashes ')
    description = models.TextField()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('feat_type_detail', [], {'id': self.id})


class Feat(models.Model):
    name = models.CharField(max_length=30)
    altname = models.SlugField(max_length=30,
        help_text='URL version of the name; use only alphanumeric char, dashes '
                  'and keep the text in lowercase except for roman numerals.')
    type = models.ForeignKey(FeatType,
        help_text='Type of feat, for example "Metamagic"')
    short_description = models.CharField(max_length=128,
        help_text='Short description shown in feat lists')
    prerequisite_feats = models.ManyToManyField("self",
        symmetrical=False, blank=True,
        help_text='An other feat or feats that the character must have in order '
                  'to acquire this feat')
    prerequisite_description = models.TextField(blank=True)
    benefit = models.TextField()
    normal = models.TextField(blank=True)
    special = models.TextField(blank=True)
    source = models.ForeignKey(Source, blank=True,
        help_text='Selecet the source book that contain the feat')
    source_page = models.IntegerField(blank=True,
        help_text='Numer page from the source book')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('feat_detail', [], {'id': self.id})
