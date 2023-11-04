# Argument list
argument_list = [
    "--disable-web-security",
    "--headless",
    "--no-sandbox",
    "--disable-infobars",
    "--disable-dev-shm-usage",
    "--disable-browser-side-navigation",
    "--disable-gpu",
    "--disable-features=VizDisplayCompositor"
]

# Init web options
snapshot_engine_options = webdriver.ChromeOptions()
for argument in argument_list:
    snapshot_engine_options.add_argument(argument)

# Assign user agent
user_agent = (self.user_agent
                or "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36")
snapshot_engine_options.add_argument(f"user-agent={user_agent}")