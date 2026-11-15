The generated test suite cannot execute because of the following test-code/setup error:
==================================== ERRORS ====================================
_________________ ERROR collecting tests/a8/uc/test_uc_p03.py __________________
ImportError while importing test module 'tests/a8/uc/test_uc_p03.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/a8/uc/test_uc_p03.py:27: in <module>
    from modules.patent.services.legal import (
E   ImportError: cannot import name 'prepare_response' from 'modules.patent.services.legal' (modules/patent/services/legal.py)
Repair the TEST CODE/TEST SETUP only.
Do not modify production code.
Do not alter test intent or expected results.
Do not add or remove test cases.
Do not introduce new specification information.
Make only the minimum changes required to make the frozen tests executable.
