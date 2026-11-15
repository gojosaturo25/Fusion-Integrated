The generated test suite cannot execute because of the following test-code/setup error:
==================================== ERRORS ====================================
_________________ ERROR collecting tests/a8/fr/test_fr_p17.py __________________
ImportError while importing test module 'tests/a8/fr/test_fr_p17.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/a8/fr/test_fr_p17.py:13: in <module>
    from modules.patent.models import (
E   ImportError: cannot import name 'TechnologyTransferRequest' from 'modules.patent.models' (modules/patent/models.py)
_________________ ERROR collecting tests/a8/fr/test_fr_p21.py __________________
ImportError while importing test module 'tests/a8/fr/test_fr_p21.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/a8/fr/test_fr_p21.py:14: in <module>
    from modules.patent.models import (
E   ImportError: cannot import name 'AuditLog' from 'modules.patent.models' (modules/patent/models.py)
_________________ ERROR collecting tests/a8/fr/test_fr_p22.py __________________
ImportError while importing test module 'tests/a8/fr/test_fr_p22.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/a8/fr/test_fr_p22.py:5: in <module>
    from django.core.mail import outbox
E   ImportError: cannot import name 'outbox' from 'django.core.mail' (.venv/lib/python3.12/site-packages/django/core/mail/__init__.py)
_________________ ERROR collecting tests/a8/fr/test_fr_p23.py __________________
ImportError while importing test module 'tests/a8/fr/test_fr_p23.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/a8/fr/test_fr_p23.py:5: in <module>
    from django.core.mail import outbox
E   ImportError: cannot import name 'outbox' from 'django.core.mail' (.venv/lib/python3.12/site-packages/django/core/mail/__init__.py)
Repair the TEST CODE/TEST SETUP only.
Do not modify production code.
Do not alter test intent or expected results.
Do not add or remove test cases.
Do not introduce new specification information.
Make only the minimum changes required to make the frozen tests executable.
