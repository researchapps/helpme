'''

Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from helpme.main import HelperBase
from helpme.action import ( record_asciinema, upload_asciinema )
from helpme.utils import ( envars_to_markdown, generate_keypair )
from helpme.logger import ( bot )
from .utils import( create_post, request_token )
import os
import pgpy
import sys

class Helper(HelperBase):

    def __init__(self, **kwargs):
 
        self.name = "discourse"

        # Discourse needs a keypair, generate if not found
        self.keypair = self._generate_keys()
        super(Helper, self).__init__(**kwargs)

    def load_secrets(self):
        self.token = self._get_and_update_setting('HELPME_DISCOURSE_TOKEN')

        # If the user doesn't have a token, generate one
        if not self.token:
            bot.info('Generating token...')

        # Load additional parameters for board category and name
        self._update_envars()


    def _update_envars(self):
        '''load additional variables from the environment, including a board
           and a category. If not set, we will then look at positionals for
           the board. If not set after positions, we prompt the user.
        '''
                  # Environment variable     # config setting under discourse
        items = [('HELPME_DISCOURSE_BOARD', 'user_prompt_board'),
                 ('HELPME_DISCOURSE_CATEGORY', 'user_prompt_category'),
                 ('HELPME_DISCOURSE_USERNAME', 'user_prompt_username')]

        self._load_envars(items)
        
    def check_env(self, envar, value):
        '''ensure that variable envar is set to some value, 
           otherwise exit on error.
        
           Parameters
           ==========
           envar: the environment variable name
           value: the setting that shouldn't be None
        '''
        if value is None:
            bot.error('You must export %s to use Discourse' % envar)
            print('https://vsoch.github.io/helpme/helper-github')
            sys.exit(1)


    def _generate_keys(self):
        '''the discourse API requires the interactions to be signed, so we 
           generate a keypair on behalf of the user
        '''
        from helpme.defaults import HELPME_CLIENT_SECRETS
        keypair_dir = os.path.join(os.path.dirname(HELPME_CLIENT_SECRETS),
                                   'discourse')

        # We store the private and public keys separately
        keypair_name = 'hmpgp'
        key_public = os.path.join(keypair_dir, "%s.pub" % keypair_name)
        key_private = os.path.join(keypair_dir, "%s.priv" % keypair_name)

        # We likely won't have generated it on first use!
        if not os.path.exists(key_public) or not os.path.exists(key_private):
            bot.info('Generating keypair for hashing requests!')
            key_pub, key_priv = generate_keypair(self.name, keypair_dir, keypair_name)           
        else:
            key_pub, _ = pgpy.PGPKey.from_file(key_public)
            key_priv, _ = pgpy.PGPKey.from_file(key_private)

        # Save to the client for later signing
        self.keypub = key_pub
        self.keypriv = key_priv


    def _start(self, positionals):

        # If the user provides a discourse board, use it.

        if positionals:

            # Let's enforce https. If the user wants http, they can specify it
            board = positionals.pop(0)
            if not board.startswith('http'):
                board = 'https://%s' % board

            self.data['user_prompt_board'] = board
            self.config.remove_option('discourse','user_prompt_board')

            # If the user provides another argument, it's the category
            if len(positionals) > 0:
                category = positionals.pop(0)
                self.data['user_prompt_category'] = category
                self.config.remove_option('discourse','user_prompt_category')
             

    def _submit(self):
        '''submit the question to the board. When we get here we should have 
           (under self.data)
           
                {'record_environment': [('DISPLAY', ':0')],
                 'user_prompt_board': 'http://127.0.0.1',
                 'user_prompt_issue': 'I want to know why dinosaurs are so great!',
                 'user_prompt_title': 'Why are dinosaurs so great?'}

           self.token should be propogated with the personal access token
        ''' 
        body = self.data['user_prompt_issue']
        title = self.data['user_prompt_title']
        board = self.data['user_prompt_board']
        username = self.data['user_prompt_username']
        category = self.data['user_prompt_category']

        # Step 1: Environment

        envars = self.data.get('record_environment')        
        body = body + envars_to_markdown(envars)

        # Step 2: Asciinema

        asciinema = self.data.get('record_asciinema')
        if asciinema not in [None, '']:
            url = upload_asciinema(asciinema)
               
            # If the upload is successful, add a link to it.

            if url is not None:
                body += "\n[View Asciinema Recording](%s)" % url
 
        # Add other metadata about client

        body += "\n\ngenerated by [HelpMe](https://vsoch.github.io/helpme/)"
        body += "\nHelpMe Discourse Id: %s" %(self.run_id)

        # Submit the issue

        post = create_post(title, body, board, category, username, self.token)
        return post
