from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
import datetime


# Structure based on National Nutrient Database for Standard Reference
# source: https://www.ars.usda.gov/Services/docs.htm?docid=8964


# Based on Table 4 - Food Description File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# models.DecimalField(max_digits=13, decimal_places=3).contribute_to_class(Food, 'calories')

class Food(models.Model):

    class Meta:
        verbose_name = _('Fooddescription')
        verbose_name_plural = _('Fooddescriptions')
    id = models.CharField(_("Nutrient Databank number"), db_column="NDB_No", max_length=5, primary_key=True, help_text=_(
        "5-digit NutrientDatabank number that uniquelyidentifies a food item. If this field is defined asnumeric, the leading zero will be lost. "))
    food_group = models.ForeignKey('FoodGroup', db_column="FdGrp_Cd", help_text=_(
        "4-digit code indicating food group to which a food item belongs. "), on_delete=models.CASCADE)
    long_description = models.CharField(_("Long description"), db_column="Long_Desc",
                                        max_length=200, help_text=_("200-character description of food item. "))
    calories = models.DecimalField(max_digits=13, decimal_places=3)
    insulin_load = models.DecimalField(max_digits=13, decimal_places=3)
    insulinogenic = models.DecimalField(max_digits=13, decimal_places=3)
    ratio = models.DecimalField(max_digits=13, decimal_places=3)
    energy_density =  models.DecimalField(max_digits=6, decimal_places=2)
    nd_weight =  models.DecimalField(max_digits=6, decimal_places=2)
    nd_calorie =  models.DecimalField(max_digits=6, decimal_places=2)
    il_score = models.DecimalField(max_digits=6, decimal_places=2)
    ed_score = models.DecimalField(max_digits=6, decimal_places=2)
    wilders_formula = models.DecimalField(max_digits=6, decimal_places=2)
    tags = TaggableManager()
    ingredient_name = models.CharField(max_length=200,blank=True, null=True)
    slug = models.CharField(blank=True, max_length=255)
    ketonumber = models.DecimalField(max_digits=5, decimal_places=2)
    il_optimiser_score = models.DecimalField(max_digits=6, decimal_places=2)
    ed_optimiser_score = models.DecimalField(max_digits=6, decimal_places=2)
    optimiser_name = models.CharField(max_length=200,blank=True, null=True)
    insulin_load_optimiser = models.DecimalField(max_digits=13, decimal_places=3)
    insulinogenic_optimiser = models.FloatField(blank=True, null=True)
    def __unicode__(self):
        return unicode(self.short_description)

    def get_absolute_url(self):
        return '/foods/micronutrients-for-'+self.slug
# Based on Table 5 - Food Group Description File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class FoodGroup(models.Model):

    class Meta:
        verbose_name = _('Food group')
        verbose_name_plural = _('Food groups')
        ordering = ['name']
    id = models.CharField(_("Food Group ID"), db_column="FdGrp_Cd", max_length=4, primary_key=True, help_text=_(
        "4-digit code identifying a food group. Only the first 2 digits are currently assigned. In the future, the last 2 digits may be used. Codes may not be consecutive. "))
    name = models.CharField(_("Name"), db_column="FdGrp_Desc",
                            max_length=60, help_text=_("Name of food group."))

    def __unicode__(self):
        return self.name


# Based on Table 6 - LanguaL Factor File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class FoodLanguaLFactor(models.Model):

    class Meta:
        verbose_name = _('Food LanguaL factor')
        verbose_name_plural = _('Food LanguaL factors')
        unique_together = ("food", "langual_factor")
    food = models.ForeignKey('Food', db_column="NDB_No", help_text=_(
        "5-digit NutrientDatabank number that uniquelyidentifies a food item. If this field is defined asnumeric, the leading zero will be lost. "), on_delete=models.CASCADE)
    langual_factor = models.ForeignKey('LanguaLFactor', db_column="Factor_Code", help_text=_(
        "The LanguaL factor from the Thesaurus."), on_delete=models.CASCADE)

    def __unicode__(self):
        return "%s - %s" % (self.food, self.langual_factor)


# Based on Table 7 - LanguaL Factor Description File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class LanguaLFactor(models.Model):

    class Meta:
        verbose_name = _('LanguaL factor')
        verbose_name_plural = _('LanguaL factors')
        ordering = ['name']
    id = models.CharField(_("Factor ID"), db_column="Factor_Code", max_length=5, primary_key=True, help_text=_(
        " TheLanguaL factor from the Thesaurus. Only thosecodes used to factor the foods contained in theLanguaL Factor file are included in this file."))
    name = models.CharField(_("Description"), db_column="Description", max_length=140, help_text=_(
        "The description of the LanguaL Factor Code from the thesaurus "))

    def __unicode__(self):
        return self.name


# Based on Table 8 - Nutrient Data File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class NutrientData(models.Model):

    class Meta:
        verbose_name = _('Nutrient Data')
        verbose_name_plural = _('Nutrient Datas')
        unique_together = ("food", "nutrient")
    food = models.ForeignKey('Food', db_column="NDB_No",
                             help_text=_("5-digit Nutrient Databank number."), on_delete=models.CASCADE)
    nutrient = models.ForeignKey('Nutrient', db_column="Nutr_No", help_text=_(
        "Unique 3-digit identifier code for a nutrient. "), on_delete=models.CASCADE)
    raw_nd_calorie =  models.DecimalField(max_digits=11, decimal_places=3)
    adjusted_nd_calorie =  models.DecimalField(max_digits=11, decimal_places=3)
    optimiser_nd_calorie = models.DecimalField(max_digits=11, decimal_places=3)
    raw_nd_weight =  models.DecimalField(max_digits=11, decimal_places=3)
    adjusted_nd_weight =  models.DecimalField(max_digits=11, decimal_places=3)
    ounce = models.DecimalField(_("Ounce"), db_column="Nutr_Val", max_digits=13,
                                decimal_places=3, help_text=_("Amount in 100 grams, edible portion."))
    data_type = models.ForeignKey(
        'Source', db_column="Src_Cd", help_text=_("Code indicating type of data."), on_delete=models.CASCADE)
    
    def __unicode__(self):
        return "%s - %s" % (self.food, self.nutrient)


# Based on Table 9 - Nutrient Definition File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Nutrient(models.Model):

    class Meta:
        verbose_name = _('Nutrient')
        verbose_name_plural = _('Nutrients')
        ordering = ['name']
    id = models.CharField(_("Nutrient ID"), db_column="Nutr_No", max_length=3,
                          primary_key=True, help_text=_("Unique 3-digit identifier code for a nutrient. "))
    units = models.CharField(_("Units"), db_column="Units", max_length=7, help_text=_(
        " Units of measure (mg, g, and so on)."))
    tagname = models.CharField(_("Tagname"), db_column="Tagname", max_length=20, blank=True, null=True, help_text=_(
        " International Network of Food Data Systems(INFOODS) Tagnames. A unique abbreviation for anutrient/food component developed by INFOODS toaid in the interchange of data."))
    name = models.CharField(_("Name"), db_column="NutrDesc",
                            max_length=60, help_text=_("Name of nutrient/food component."))
    decimals = models.IntegerField(_("Decimals"), db_column="Num_Dec", max_length=1, help_text=_(
        "Number of decimal places to which a nutrient value is rounded. "))
    order = models.IntegerField(_("Order"), db_column="SR_Order", max_length=6, help_text=_(
        "Used to sort nutrient records in the same order as various reports produced from SR. "))
    rdi = models.DecimalField(max_digits=13, decimal_places=3)
    rdi_male = models.DecimalField(max_digits=7, decimal_places=3)
    rdi_female = models.DecimalField(max_digits=7, decimal_places=3)
    oni_male = models.DecimalField(max_digits=7, decimal_places=3)
    oni_female = models.DecimalField(max_digits=7, decimal_places=3)
    rdi_kg = models.DecimalField(max_digits=7, decimal_places=3)
    rdi_75 = models.DecimalField(max_digits=7, decimal_places=3)
    rdi_100 = models.DecimalField(max_digits=7, decimal_places=3)
    rdi_pregnant = models.DecimalField(max_digits=7, decimal_places=3)
    rdi_breast = models.DecimalField(max_digits=7, decimal_places=3)
    slug = models.CharField(blank=True, max_length=255)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return '/top-100-foods-and-recipes-high-in-'+self.slug

# Based on Table 10 - Source Code File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Source(models.Model):

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')
        ordering = ['name']
    id = models.CharField(_("Source ID"), db_column="Src_Cd",
                          max_length=2, primary_key=True, help_text=_("2-digit code."))
    name = models.CharField(_("Name"), db_column="SrcCd_Desc", max_length=60, help_text=_(
        "Description of source codethat identifies the type ofnutrient data. "))

    def __unicode__(self):
        return self.name


# Based on Table 11 - Derivation Code File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Derivation(models.Model):

    class Meta:
        verbose_name = _('Derivation')
        verbose_name_plural = _('Derivations')
        ordering = ['name']
    id = models.CharField(_("Derivation ID"), db_column="Deriv_Cd",
                          max_length=4, primary_key=True, help_text=_("4-digit code"))
    name = models.CharField(_("Name"), db_column="Deriv_Desc", max_length=120, help_text=_(
        "Description of derivation code giving specific information on how the value was determined. "))

    def __unicode__(self):
        return self.name


# Based on Table 12 - Weight Code File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Weight(models.Model):

    class Meta:
        verbose_name = _('LanguaL factor')
        verbose_name_plural = _('LanguaL factors')
        ordering = ['name']
        unique_together = ("food", "sequence")
    food = models.ForeignKey('Food', db_column="NDB_No",
                             help_text=_("5-digit Nutrient Databank number."), on_delete=models.CASCADE)
    sequence = models.CharField(
        _("Sequence"), db_column="Seq", max_length=5, help_text=_("Sequence number."))
    amount = models.DecimalField(_("Amount"), db_column="Amount", max_digits=8,
                                 decimal_places=3, help_text=_("Unit modifier (for example, 1 in '1 cup'). "))
    name = models.CharField(_("Name"), db_column="Msre_Desc", max_length=84, help_text=_(
        "Description (for example, cup, diced, and 1-inch pieces). "))
    grams = models.DecimalField(_("Grams"), db_column="Gm_Wgt",
                                max_digits=8, decimal_places=1, help_text=_("Gram weight."))
    data_points = models.IntegerField(_("Data points"), db_column="Num_Data_Pts",
                                      max_length=3, blank=True, null=True, help_text=_("Number of data points. "))
    standard_derivation = models.DecimalField(
        _("Derivation (Standard)"), db_column="Std_Dev", max_digits=10, decimal_places=3, blank=True, null=True)

    def __unicode__(self):
        return self.name


# Based on Table 13 - Footnote File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

FOOTNOTE_CHOICES = (
    ('D', _('Footnote adding information to the food description')),
    ('M', _('Footnote adding information to measure description')),
    ('N', _(
        'Footnote providing additional information on a nutrient value')),
)


class Footnote(models.Model):

    class Meta:
        verbose_name = _('LanguaL factor')
        verbose_name_plural = _('LanguaL factors')
        ordering = ['name']
    food = models.ForeignKey('Food', db_column="NDB_No",
                             help_text=_("5-digit Nutrient Databank number."), on_delete=models.CASCADE)
    sequence = models.CharField(_("Sequence"), db_column="Footnt_No", max_length=4, help_text=_(
        " Sequence number. Ifa given footnote applies tomore than one nutrient number, the same footnotenumber is used. As a result, this file cannot beindexed. "))
    type = models.CharField(_("Type"), db_column="Footnt_Typ", max_length=1, choices=FOOTNOTE_CHOICES, help_text=_(
        "Type of footnote:D = footnote adding information to the fooddescription;M = footnote adding information to measuredescription;N = footnote providing additional information on anutrient value. If the Footnt_typ = N, the Nutr_No willalso be filled in. "))
    nutrient = models.ForeignKey('Nutrient', db_column="Nutr_No", blank=True, null=True, help_text=_(
        " Unique 3-digit identifier code for a nutrient to which footnote applies. "), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), db_column="Footnt_Txt",
                            max_length=200, help_text=_("Footnote text."))

    def __unicode__(self):
        return self.name


# Based on Table 14 - Data Link File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class DataLink(models.Model):

    class Meta:
        verbose_name = _('Data link')
        verbose_name_plural = _('Data links')
        unique_together = ("food", "nutrient", 'data_source')
    food = models.ForeignKey('Food', db_column="NDB_No",
                             help_text=_("5-digit Nutrient Databank number."), on_delete=models.CASCADE)
    nutrient = models.ForeignKey('Nutrient', db_column="Nutr_No", help_text=_(
        "Unique 3-digit identifier code for a nutrient. "), on_delete=models.CASCADE)
    data_source = models.ForeignKey('DataSource', db_column="DataSrc_ID", help_text=_(
        "Unique ID identifying the reference/source. "), on_delete=models.CASCADE)

    def __unicode__(self):
        return "%s - %s - %s" % (food, nutrient, data_source)


# Based on Table 15 - Data File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class DataSource(models.Model):

    class Meta:
        verbose_name = _('Data source')
        verbose_name_plural = _('Data sources')
        ordering = ['name']
    id = models.CharField(_("DataSource ID"), db_column="DataSrc_ID", max_length=6,
                          primary_key=True, help_text=_("Unique number identifying the reference/source. "))
    authors = models.CharField(_("Authors"), db_column="Authors", max_length=255, blank=True, null=True, help_text=_(
        "List of authors for a journal article or name of sponsoring organization for other documents. "))
    name = models.CharField(_("Name"), db_column="Title", max_length=255, blank=True, null=True, help_text=_(
        "Title of article or name of document, such as a report from a company or trade association. "))  # optional to make the import work
    year = models.IntegerField(_("Year"), db_column="Year", max_length=4,
                               blank=True, null=True, help_text=_(" Year article or document was published."))
    journal = models.CharField(_("Journal"), db_column="Journal", max_length=135,
                               blank=True, null=True, help_text=_("Name of the journal in which the article was published. "))
    volume = models.CharField(_("Volume"), db_column="Vol_City", max_length=16, blank=True, null=True, help_text=_(
        " Volume number for journal articles, books, or reports; city where sponsoring organization is located. "))
    issue_state = models.CharField(_("Issue (state)"), db_column="Issue_State", max_length=5, blank=True, null=True, help_text=_(
        " Issue number for journal article; State where the sponsoring organization is located. "))
    start_page = models.IntegerField(_("Start page"), db_column="Start_Page", max_length=5,
                                     blank=True, null=True, help_text=_("Starting page number of article/document. "))
    end_page = models.IntegerField(_("End page"), db_column="End_Page", max_length=5,
                                   blank=True, null=True, help_text=_("Ending page number of article/document. "))

    def __unicode__(self):
        return self.name


# Based on Table 16 - Abbreviated File
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Not required for relational databases


# Based on Table 17 - Foods Deleted
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class DeletedFood(models.Model):

    class Meta:
        verbose_name = _('Deleted food')
        verbose_name_plural = _('Deleted foods')
        ordering = ['name']
    food_id = models.CharField(_("Nutrient Databank number"), db_column="NDB_No", max_length=5,
                               primary_key=True, help_text=_("Unique 5-digit number identifying deleted item. "))
    name = models.CharField(_("Name"), db_column="Shrt_Desc", max_length=60, help_text=_(
        "60-character abbreviated description of food item. "))

    def __unicode__(self):
        return self.name


# Based on Table 18 - Nutrients Deleted
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class DeletedNutrient(models.Model):

    class Meta:
        verbose_name = _('Deleted nutrient')
        verbose_name_plural = _('Deleted nutrients')
        ordering = ['nutrient_id']
    food_id = models.CharField(_("Nutrient Databank number"), db_column="NDB_No", max_length=5, primary_key=True, help_text=_(
        "Unique 5-digit number identifying the item that contains the deleted nutrient record. "))
    nutrient_id = models.CharField(_("Nutrient ID"), db_column="Nutr_No",
                                   max_length=3, help_text=_("Nutrient number of deleted record. "))

    def __unicode__(self):
        return self.nutrient_id


# Based on Table 19 - Footnotes Deleted
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class DeletedFootnote(models.Model):

    class Meta:
        verbose_name = _('LanguaL factor')
        verbose_name_plural = _('LanguaL factors')
    food_id = models.CharField(_("Nutrient Databank number"), db_column="NDB_No", max_length=5, primary_key=True, help_text=_(
        "Unique 5-digit number identifying the item that contains the deleted nutrient record. "))
    sequence = models.CharField(
        _("Sequence"), db_column="Footnt_No", max_length=4)
    type = models.CharField(_("FootnoteType"), db_column="Footnt_Typ", max_length=1,
                            choices=FOOTNOTE_CHOICES, help_text=_("Type of footnote of deleted record. "))

    def __unicode__(self):
        return "%s - %s" % (self.food_id, self.sequence)
