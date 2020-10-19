from import_export import resources
from .models import Profession, Formation, Location, Diplome

class ProfessionResource(resources.ModelResource):
	class Meta:
		model = Profession

class FormationResource(resources.ModelResource):
	class Meta:
		model = Formation

class LocationResource(resources.ModelResource):
	class Meta:
		model = Location

class DiplomeResource(resources.ModelResource):
	class Meta:
		model = Diplome