# Readme
Web Scraper which collects data from a given website and saving it to a JSON File.
I made two options.

## Installation

Python 3 should be installed.

    https://github.com/Oomamchur/UData_test_task
    cd UData_test_task
    python -m venv venv

On Windows:

    source venv\Scripts\activate

On macOS or Linux:

    source venv/bin/activate

Install requirements:

    pip install -r requirements.txt

## First Option
File async.py. This func is asynchronous and retrieves data from a response. 
It's fast but doesn't fetch the data in the format specified in the task.

    python async.py

## Second Option
File main.py. This func extracts data from HTML code using Selenium because it provides detailed information.

    python main.py