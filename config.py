# This file is not strictly required, but provides a centralized
# location for configuration settings.  It's good practice to
# separate configuration from code.

import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///tasks.db")

# You could add other configuration settings here, such as API keys,
# port numbers, etc.