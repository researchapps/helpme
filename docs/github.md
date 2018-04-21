# Usage

Github is the default client. To use Github, 
[create a personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/).
You can call it whatever you like (`helpme-client` in the example below) and request permissions for "gist" and
"notifications."

![img/github-token.png](img/github-token.png)

Click "Generate Token", and when you have the token, export it to your environment:

```bash
export HELPME_GITHUB_TOKEN=xxxxx
```

The token will be found the first time you run the client, and cached in your `$HOME/helpme.cfg`
file. If you are interested in how this works, see the [developer](developer.md) documentation.