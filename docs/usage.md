# Usage

See general help

```bash
helpme

[github] HelpMe Command Line Tool v0.0.1
usage: helpme [-h] [--debug] [--version] [--quiet]
              {list,config} ... [{github,uservoice}]

HelpMe Command Line Tool

positional arguments:
  {github,uservoice}

optional arguments:
  -h, --help          show this help message and exit
  --debug             use verbose logging to debug.
  --version           show version and exit.
  --quiet             suppress additional output.

actions:
  actions for HelpMe Command Line Tool

  {list,config}       helpme actions
    list              show installed helpers
    config            configure a helper
```

List the helpers installed

```bash
$ helpme list
Helpers Installed:
github
uservoice
```

Interactive help from a specific helper (e.g., Github helper):

```bash
$ helpme github
```