from django.contrib import admin
from .models import Team, League, Match, Tournament
from django.utils.safestring import mark_safe


@admin.register(Match)
class MatchInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'match_score', 'match_tournament', 'date_time')
    list_display_links = ('title', 'match_tournament',)
    list_filter = ('tournament',)

    def match_tournament(self, obj):
        return obj.tournament.title

    def match_score(self, obj):
        if obj.status:
            return str(obj.team_1_goals)+' : '+str(obj.team_2_goals)
        else:
            return ''

    match_tournament.short_description = 'Tournament'
    match_tournament.admin_order_field = 'Tournament'
    match_score.short_description = 'Score'
    match_score.admin_order_field = 'Score'


@admin.register(Tournament)
class MatchInfoAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Team)
class TeamInfoAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'team_league')
    list_display_links = ('image_tag', 'title', 'team_league')
    list_filter = ('league',)

    def team_league(self, obj):
        return obj.league.title

    team_league.short_description = 'League'
    team_league.admin_order_field = 'league'


@admin.register(League)
class LeagueInfoAdmin(admin.ModelAdmin):
    # readonly_fields = ('image')
    list_display = ('image_tag', 'title')
