from TwitterAPI import TwitterAPI
from BaseNotifier import BaseNotifier


class TwitterNotifier(BaseNotifier):
    """
    This notification plugin notifies users via Twitter direct messages.

    Note that you can only send direct messages to your followers. The
    alternative would be to send @replies, but Twitter Automation rules and
    best practices [1] require prior opt-in from the users who are
    automatically mentioned, which is most often impractical. Furthermore, the
    assumption that owners of Freifunk nodes are following the corresponding
    Twitter account is reasonable.

    The needed keys can be generated and obtained from [2]. Note that you need
    to generate an Access token that is allowed to access direct messages.

    [1] https://support.twitter.com/articles/76915
    [2] https://app.twitter.com/

    :config api_key The API key for an app
    :config api_secret The API secret for an app
    :config access_token_key The access token for your account
    :config access_token_secret The access token secret for your account
    """

    regex = re.compile('^@([A-Za-z_][A-Za-z0-9_]+)$')
    api_base = 'https://api.twitter.com/1.1/'

    def __init__(self, config):
        self.config = config
        self.api = TwitterAPI(
            self.config['api_key'],
            self.config['api_secret'],
            self.config['access_token_key'],
            self.config['access_token_secret'],
        )

    def notify(self, contact, node):
        req = self.api.request('direct_messages/new', {
            'screen_name': self.regex.match(contact).group(1),
            'text': node.format_infotext(self.config['text']),
        })

        return req.status_code == 200
