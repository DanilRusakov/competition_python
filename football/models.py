import simplejson as json
from django.db import models
from django.utils.html import format_html
from django.utils.timezone import now
from django.db.models.signals import post_save


class League(models.Model):
    class Meta:
        verbose_name = 'League'
        verbose_name_plural = 'Leagues'

    title = models.CharField(unique=True, max_length=50)
    image = models.ImageField(upload_to='uploads/leagues/', default='no-image.png')

    # To show the media files in the list display in the admin panel:
    def image_tag(self):
        return format_html('<img src="{0}" width="50" height="50" />'.format(self.image.url))

    image_tag.allow_tags = True

    # image_tag.short_description = 'Image'

    def __str__(self):
        return f'{self.title}'


class Team(models.Model):
    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    title = models.CharField(unique=True, max_length=50)
    image = models.ImageField(upload_to='uploads/teams/', default='no-image.png')
    information = models.TextField(null=True, max_length=500, blank=True)
    league = models.ForeignKey(
        League,
        related_name='League',
        on_delete=models.SET_NULL,
        null=True,
    )

    # To show the media files in the list display in the admin panel:
    def image_tag(self):
        return format_html('<img src="{0}" title="{1}" width="50" height="50" />'.format(self.image.url, self.title))

    image_tag.allow_tags = True

    def __str__(self):
        return f'{self.title}'


class Tournament(models.Model):
    GRID_8X8 = '8x8'
    GRID_4X4 = '4x4'
    TABLE = 'table'

    TOURNAMENT_TYPES = [
        # (GRID_16X16, '16x16'),
        (TABLE, 'Table'),
        (GRID_4X4, 'GRID 8 Teams'),
        (GRID_8X8, 'GRID 16 Teams'),
    ]

    class Meta:
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'

    title = models.CharField(max_length=50, unique=True)
    info = models.TextField(null=True)
    teams_in = models.ManyToManyField(Team, )
    date_time = models.DateTimeField(default=now, blank=True)
    type = models.CharField(
        max_length=5,
        choices=TOURNAMENT_TYPES,
        default=TABLE,
    )

    def save(self, *args, **kwargs):
        print('---------')
        print(self.title)
        print('---------')
        # TODO check if teams_in
        super(Tournament, self).save(*args, *kwargs)

    def __str__(self):
        return f'{self.title} type:{self.type}'


class Match(models.Model):
    MATCH_STATUS = (
        (0, 'Pending'),
        (1, 'Done'),
    )

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    title = models.CharField(max_length=50)
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
    )
    team_1 = models.ForeignKey(
        Team,
        related_name='Team_1',
        on_delete=models.CASCADE,
    )
    team_2 = models.ForeignKey(
        Team,
        related_name='Team_2',
        on_delete=models.CASCADE,
    )
    team_1_goals = models.SmallIntegerField(
        default=0,
    )
    team_2_goals = models.SmallIntegerField(
        default=0,
    )
    status = models.SmallIntegerField(choices=MATCH_STATUS, default=0)
    date_time = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f'{self.title}'


def update_tournament_team_info(tournament_id):
    TournamentTeamInfo.objects.filter(tournament=tournament_id).update(
        won=0, matches=0, drawn=0, lost=0, goal_scored=0, goal_conceded=0, points=0,
    )
    matches = Match.objects.filter(tournament=tournament_id)
    for match in matches:
        if match.status == 0:
            return
        team_1 = TournamentTeamInfo.objects.get(team=match.team_1, tournament=tournament_id)
        team_2 = TournamentTeamInfo.objects.get(team=match.team_2, tournament=tournament_id)
        team_1.matches += 1
        team_1.goal_scored += match.team_1_goals
        team_1.goal_conceded += match.team_2_goals
        team_2.matches += 1
        team_2.goal_scored += match.team_2_goals
        team_2.goal_conceded += match.team_1_goals
        if match.team_1_goals > match.team_2_goals:
            team_1.won += 1
            team_1.points += 3
            team_2.lost += 1
        elif match.team_1_goals < match.team_2_goals:
            team_1.lost += 1
            team_2.won += 1
            team_2.points += 3
        else:
            team_1.drawn += 1
            team_2.drawn += 1
            team_1.points += 1
            team_2.points += 1
        team_1.save()
        team_2.save()


class TournamentTeamInfo(models.Model):
    class Meta:
        verbose_name = 'Team Info'
        verbose_name_plural = 'Teams Info'

    team = models.ForeignKey(
        Team,
        related_name='Team',
        on_delete=models.CASCADE,
    )
    matches = models.SmallIntegerField(
        default=0
    )
    won = models.SmallIntegerField(
        default=0
    )
    drawn = models.SmallIntegerField(
        default=0
    )
    lost = models.SmallIntegerField(
        default=0
    )
    goal_scored = models.SmallIntegerField(
        default=0
    )
    goal_conceded = models.SmallIntegerField(
        default=0
    )
    points = models.SmallIntegerField(
        default=0
    )
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        default=1,
    )


# TODO: create methods save inside models instead signals
# SIGNALS
# signal create matches
def create_tournament_matches(instance, created, **kwargs):
    # if not created:
    #     return
    teams_in = instance.teams_in.all()
    print(teams_in)
    print('----------------------------------------------------')
    print(instance.teams_in)
    print('----------------------------------------------------')
    for team_1 in teams_in:
        for team_2 in teams_in:
            if team_1.id is not team_2.id:
                match_title = '{} vs {}'.format(team_1.title, team_2.title)
                Match.objects.create(title=match_title, tournament=instance, team_1=team_1, team_2=team_2)


# post_save.connect(create_tournament_matches, sender=Tournament)


def create_tournament_team_info(instance, created, **kwargs):
    if not created:
        return
    json_dec = json.decoder.JSONDecoder()
    teams_ids = json_dec.decode(instance.teams)
    teams_list = Team.objects.filter(pk__in=teams_ids)
    for team in teams_list:
        TournamentTeamInfo.objects.create(team=team, tournament=instance)


# post_save.connect(create_tournament_team_info, sender=Tournament)


