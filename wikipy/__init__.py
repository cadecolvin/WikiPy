import json
import requests


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

    def get_page_text(self, page_id):
        """
        Returns the full text of the requested page.
        """
        payload = {'action':'query',
                   'format':'json',
                   'pageids':page_id,
                   'prop':'revisions',
                   'rvprop':'content'}

        r = requests.post(self.url, data=payload, cookies=self.cookies)
        if r.status_code != 200:
            raise Exception

        response = r.json()
        page = response['query']['pages'][str(page_id)]
        return page['revisions'][0]['*']

    def get_category_pages(self, category_name):
        """
        Returns all page titles that fall under the specified category
        """
        payload = {'action':'query',
                   'format':'json',
                   'list':'categorymembers',
                   'cmtitle':'Category:' + category_name,
                   'cmlimit':'500'}

        r = requests.post(self.url, data=payload, cookies=self.cookies)
        if r.status_code != 200:
            raise Exception

        response = r.json()
        members = response['query']['categorymembers']
        pages = []
        for page in members:
            pages.append((page['pageid'], page['title']))

        return pages
