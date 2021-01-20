import re
import discogs_api
from fuzzywuzzy import process

track = dict.fromkeys([
    'artist',
    'track_title',
    'track_position',
    'label',
    'release_title',
    'release_year',
    'release_id'])


class Identifier:

    def __init__(self, use_discogs=True):
        self.use_discogs = use_discogs

    def search(self, expression, artist=None, track_title=None, pos=None, release_title=None, release_id=None):

        if self.use_discogs:
            track = self._search_discogs(expression)

        return track

    def _search_discogs(self, search_str):

        track = dict.fromkeys([
            'artist',
            'track_title',
            'track_position',
            'label',
            'release_title',
            'release_year',
            'release_id'])

        d = discogs_api.Client('vinylbox/0.1', user_token="jvtwTwooUJnzVTngCZmInzhCBUlfiULHOmWHmhYU")
        r = re.search('(.*)\s-\s(.*)', search_str)
        search_str_artist = r.group(1)
        search_str_track = r.group(2)
        # results = d.search(artist=search_str_artist, track=search_str_track)
        results = d.search(search_str)
        #for results_idx in range(results.count):
        for results_idx in range(0):

            release = results[results_idx]
            release_title = release.title
            tracklist = release.tracklist
            fuzzy_match = process.extract(search_str_track,
                                          {idx: track.title for track, idx in zip(tracklist, range(len(tracklist)))},
                                          limit=1)
            if fuzzy_match:
                track = tracklist[fuzzy_match[0][2]]
                track['track_title'] = track.title
                track['track_position'] = track.position
                track_artists = track.artists
            else:
                print('Track could not be found in tracklist')

        return track