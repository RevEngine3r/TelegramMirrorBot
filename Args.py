import argparse


class Args:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=
            'Mirror Telegram Channel.')

        self.parser.add_argument('--mt_proxy', '-p', help='Use built-in MTProxy Server.', action='store_true')
        self.parser.add_argument('--iter_messages', '-i', help='Run Iter Messages Action.', action='store_true')
        self.parser.add_argument('--config', '-c', help='Run Download NOW.', type=str, default='default',
                                 action='store')

        self.args = self.parser.parse_args()

    @property
    def mt_proxy(self):
        return self.args.__dict__['mt_proxy']

    @property
    def iter_messages(self):
        return self.args.__dict__['iter_messages']

    @property
    def run_now(self):
        return self.args.__dict__['run_now']

    @property
    def run_test(self):
        return self.args.__dict__['run_test']

    @property
    def config(self):
        return self.args.__dict__['config']


args = Args()
