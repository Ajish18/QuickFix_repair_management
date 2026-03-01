### QuickFix

QuickFix repair management

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit

A2 - Multi-Site & Configuration
site_config.json contains settings of particular site, it only applicable to that site. Example each site must have it own db passwords.
common_site_config.json The configurartion defined here will be applicable for all the sites in the same bench.
So, When we put a secret in common_site_config.json it will applicable in all sites and cause security risks.

When we start bench the procfile is read, and executes:
web-It is the web server it defines the port to run the site.
worker-Do the background jobs.
Schedulers-Do the scheduled job at a paritcular time defined.
Socket io- for real time notification, done without page reload.




