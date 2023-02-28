# AIVEN challenge
    
    Monitoring tool with ability to check specified hosts with interval frequency.
    And check http response for matching with provided regexp.
    Under the hood application uses APScheduler, asyncio, asyncpg with connection pool.
    Service outputs cloudfriendly logs. 

# Install

    pip install -r requirements.txt

# Migrations
    
    ./bin/migrate.sh

# Run
    
    ./bin/run.sh

# CI and tests
    
    ./bin/ci.sh run_all_tests

# Environment variables

    DB_NAME - database name
    DB_USER - database user
    DB_PASSWORD - database password
    DB_HOST - database host
    DB_PORT - database port
    LOG_LEVEL - logging level ("INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG")

# How to

    Set environment variables for your database creds and name.
    Set desired log level, currenlty there is only "INFO" and "WARNING" entries implemented.
    At first launch migrate database using ./bin/migrate.sh.
    Fill "websites" table with hosts to monitor.

    Start service with ./bin/run.sh command, remember to provide valid websites satisfies following rules:
        - interval between 5 and 300 seconds.
        - valid regexp.
        - valid url.

    Check results stored at web_check_results table.

# TODO 

    - Current max scheduled job count is 10, consider tuning, maybe set to website table rows count.
    - Service have simpliest possible migration tool. To provide smooth database scheme changes and versioning 
    separate migration tool can be used.
    - To retrieve websites from table, service should be restarted. That can be changed to update tasks during runtime behavior.
    - There is no dependencies separation now (dev/prod) so unnecessary packages will be installed for runtime,
    poetry with separation to dev and prod packages can fit well here.
    - pyproject.toml file - for keep all project configurations in single file(poetry, black, pytest).
    - Simpliest CI scripts used in project also, definitely should be changed with specific CI tool used by development
    (.gitlab-ci.yml, Jenkinsfile, etc.)
    - Mypy code checks for CI pipeline.
    - Url validation function should be improved.

# Attributions
    
    APScheduler asyncio usage example:

        https://github.com/agronholm/apscheduler/blob/v3.9.0/examples/schedulers/asyncio_.py
    
    Mocking python async functions:

        https://dino.codes/posts/mocking-asynchronous-functions-python/
    
    Aiohttp client tracing:
    
        https://docs.aiohttp.org/en/stable/client_advanced.html#aiohttp-client-tracing
    
    
    


    