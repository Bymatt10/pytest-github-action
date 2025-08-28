#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    os.environ.setdefault('SECRET_KEY', 'django-test-secret-key')
    os.environ.setdefault('DEBUG', 'True')
    os.environ.setdefault('ALLOWED_HOSTS', 'localhost,127.0.0.1')
    
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["stations.tests"])
    
    if failures:
        sys.exit(bool(failures))
