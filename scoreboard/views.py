from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic

from scoreboard.models import Player
from scoreboard.models import Score
from scoreboard.models import Song


class Songs(generic.ListView):
    """
    List all songs
    """
    model = Song
    context_object_name = 'songs'
    template_name = 'scoreboard/songs.html'
    paginate_by = 20


def song(request, song_id):
    """
    Song scores
    """
    song = get_object_or_404(Song, slug=song_id)
    return render(request, 'scoreboard/song.html', { 'song': song })


class Players(generic.ListView):
    """
    List all players
    """
    model = Player
    context_object_name = 'players'
    template_name = 'scoreboard/players.html'
    paginate_by = 20


def player(request, player_name):
    """
    Player info
    """
    player = get_object_or_404(Player, name=player_name)
    positions = dict()  # will contain { song: { difficulty: { score: position } } }

    # get all played songs (in Score objects)
    scores_player = player.score_set.order_by('song').only('song').distinct()
    for score_player in scores_player:
        song = score_player.song
        positions[song] = dict()  # will contain { difficutly: { score: position } }
        # get all scores for the song
        scores_song = Score.objects.filter(song=song)
        # get difficulties
        scores_song_player = scores_song.filter(player=player).order_by('-difficulty').only('difficulty').distinct()
        for score_song_player in scores_song_player:
            difficulty = score_song_player.difficulty
            difficulty_val = score_song_player.get_difficulty_display()
            # get all scores for the song and the difficulty
            scores = scores_song.filter(difficulty=difficulty).order_by('-score')
            # get all scores for the song, the difficulty and the player
            player_scores = scores.filter(player=player).order_by('-score')
            # get positions
            player_positions = {score: list(scores).index(score) + 1 for score in player_scores}

            # save positions
            positions[song][difficulty_val] = player_positions  # contains { score: position }

    return render(request, 'scoreboard/player.html', { 'player': player, 'positions': positions })


def scoreboard(request):
    """
    Scoreboard summary
    """
    players = Player.objects.all()
    scores = Score.objects.all()
    songs = Song.objects.all()

    context = {
        'players': players,
        'scores': scores,
        'songs': songs,
    }

    return render(request, 'scoreboard/scoreboard.html', context)
