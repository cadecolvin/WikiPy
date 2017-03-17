import json
import requests


__version__ = '0.1'


class WikiClient():
    """
    WikiClient is a wrapper around the MediaWiki API. It should be the only
    class needed to make requests.
    """
    def __init__(self, url, username, password):
        self.url = url + '/api.php'
        self.username = username
        self.password = password

        self._login()

    def _login(self):
        """
        Logs into Mediawiki using the URL, Username, and Password created
        on init. A cookiejar containing the reponse must be passed with
        all subsequent responses

        Logging in is a two step process:
            1. Request a login token 
            2. Request a session with the token, username, and password
        """
        payload = {'action':'query',
                   'format':'json',
                   'meta':'tokens',
                   'type':'login'}

        # First, get the login token
        r = requests.post(self.url, data=payload)
        if r.status_code != 200:
            raise Exception

        self.cookies = r.cookies
        response = json.loads(r.content)
        payload['lgtoken'] = response['query']['tokens']['logintoken']

        # Next, login again passing the token
        r = requests.post(self.url, data=payload, cookies=self.cookies)

    def get_page_text(self, page_title):
        """
        Returns the full markup of the requested page.
        """
        payload = {'action':'query',
                   'format':'json',
                   'titles':page_title,
                   'prop':'revisions',
                   'rvprop':'content'}

        r = requests.post(self.url, data=payload, cookies=self.cookies)
        if r.status_code != 200:
            raise Exception

        response = r.json()
        pages = response['query']['pages']
        page_ids = list(pages.keys())
        page_text = pages[page_ids[0]]['revisions'][0]['*']
        return page_text
