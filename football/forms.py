from django import forms
from django_select2.forms import Select2MultipleWidget

from .models import Team, Tournament


class TournamentForm(forms.Form):

    class Meta:
        model = Tournament
        fields = ['title', 'teams']
    # type = forms.ModelMultipleChoiceField(queryset=Tournament.objects.all())
    title = forms.CharField(max_length=50)
    tournament_type = forms.CharField(
        widget=forms.Select(
            choices=Tournament.TOURNAMENT_TYPES
        )
    )
    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), widget=Select2MultipleWidget)

    def clean_teams(self, *args, **kwargs):
        teams = self.cleaned_data.get('teams')

        tournament_type = self.cleaned_data.get('tournament_type')

        if teams.count() < 3:
            raise forms.ValidationError("3 teams is min amount")
        if tournament_type == Tournament.GRID_4X4 and teams.count() is not 8:
            raise forms.ValidationError("This type of competition must include 8 teams")
        return teams

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Tournament.objects.filter(title=title).exists():
            raise forms.ValidationError('Current title already exist!')
        return title
