'''

Copyright (C) 2017-2018 Vanessa Sochat.

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
from helpme.logger import ( bot )
from .utils import create_issue
import os
import sys

class Helper(HelperBase):

    def __init__(self, **kwargs):
 
        self.name = "github"
        super(Helper, self).__init__(**kwargs)

    def load_secrets(self):
        self.token = self._get_and_update_setting('HELPME_GITHUB_TOKEN')
        self.check_env('HELPME_GITHUB_TOKEN', self.token)


    def check_env(self, envar, value):
        '''ensure that variable envar is set to some value, 
           otherwise exit on error.
        
           Parameters
           ==========
           envar: the environment variable name
           value: the setting that shouldn't be None
        '''
        if value is None:
            bot.error('You must export %s to use Github' %envar)
            print('https://vsoch.github.io/helpme/helper-github')
            sys.exit(1)


    def _start(self, positionals):

        # If the user provides a repository name, use it

        if positionals:
            self.data['user_prompt_repo'] = positionals[0]
            self.config.remove_option('github','user_prompt_repo')
        

    def _submit(self):
        '''submit the issue to github. When we get here we should have:
           
           {'user_prompt_issue': 'I want to do the thing.', 
            'user_prompt_repo': 'vsoch/hello-world', 
            'record_asciinema': '/tmp/helpme.93o__nt5.json',
            'record_environment': ((1,1),(2,2)...(N,N))}

           self.token should be propogated with the personal access token
        '''
 
        title = "HelpMe Github Issue: %s" %(self.run_id)
        body = self.data['user_prompt_issue']
        repo = self.data['user_prompt_repo']

        # Step 1: Environment

        envars = self.data.get('record_environment')
        if envars not in [None, '', []]:
            body += '\n## Environment\n'
            for envar in envars:
                body += ' - **%s**: %s\n' %(envar[0], envar[1])

        # Step 2: Asciinema

        asciinema = self.data.get('record_asciinema')
        if asciinema not in [None, '']:
            url = upload_asciinema(asciinema)
               
            # If the upload is successful, add a link to it.

            if url is not None:
                body += "\n[View Asciinema Recording](%s)" %url
 
        # Add other metadata about client

        body += "\ngenerated by [HelpMe](https://vsoch.github.io/helpme/)"

        # Submit the issue

        issue = create_issue(title, body, repo, self.token)
        return issue
