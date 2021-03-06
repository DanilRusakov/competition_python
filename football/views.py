from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import TournamentForm
from .models import *
import simplejson as json


class IndexView(TemplateView):
    template_name = 'football/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class TournamentsView(TemplateView):
    template_name = 'football/tournaments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournaments'] = Tournament.objects.all()
        return context


def tournament_single(request, id):
    if request.POST:
        matches = Match.objects.filter(tournament=id)
        post_data = request.POST
        for match in matches:
            match_list = post_data.getlist('match_' + str(match.id))
            match_status = post_data.get('status_' + str(match.id), 0)
            if len(match_list) == 2:
                team_1_goals = match_list[0]
                team_2_goals = match_list[1]
                # Save match
                current_match = Match.objects.get(pk=match.id)
                current_match.team_1_goals = int(team_1_goals)
                current_match.team_2_goals = int(team_2_goals)
                current_match.status = int(match_status)
                current_match.save()
        update_tournament_team_info(id)

    if Tournament.objects.filter(pk=id).exists() is not True:
        return HttpResponseRedirect(reverse('football:tournaments'))
    else:
        tournament = Tournament.objects.get(pk=id)
        teams_statistics = TournamentTeamInfo.objects.filter(tournament=id).order_by('-points')
        teams_list = tournament.teams_in.all()
        match_list = Match.objects.filter(tournament=id)

        context = {
            'tournament': tournament,
            'teams': teams_list,
            'matches': match_list,
            'statistics': teams_statistics,
        }
        return render(request, 'football/tournament.html', context)


def form_view(request):
    form = TournamentForm(request.POST or None)
    context = {'form': form}
    if request.POST and form.is_valid():
        tournament = Tournament()
        tournament.type = form.cleaned_data.get('tournament_type')
        tournament.title = form.cleaned_data.get('title')
        tournament.save()
        teams_list = []
        teams = form.cleaned_data.get('teams')
        for team in teams:
            if Team.objects.filter(pk=team.id).exists():
                teams_list.append(Team.objects.get(pk=team.id))
        tournament.teams_in.set(teams_list)
        tournament.save()
        return HttpResponseRedirect(reverse('football:tournaments'))
    return render(request, 'football/create_tournament.html', context)
