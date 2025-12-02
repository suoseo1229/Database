#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    print("=== manage.py 시작됨 ===") 
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Database.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django가 설치되어 있지 않거나 문제가 있습니다.") from exc
    execute_from_command_line(sys.argv)
