from django.conf.urls import url

from scoreboard import views


urlpatterns = [
    url(r'^$', views.scoreboard, name='scoreboard'),
    # songs
    url(r'^songs/$', views.Songs.as_view(), name='songs'),
    url(r'^songs/(?P<song_id>.+)/$', views.song, name='song'),
    # players
    url(r'^players/$', views.Players.as_view(), name='players'),
    url(r'^players/(?P<player_name>.+)$', views.player, name='player'),
]
