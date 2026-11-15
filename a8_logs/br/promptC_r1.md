The generated test suite cannot execute because of the following test-code/setup error:
==================================== ERRORS ====================================
_________________ ERROR collecting tests/a8/br/test_br_p09.py __________________
ImportError while importing test module 'tests/a8/br/test_br_p09.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/a8/br/test_br_p09.py:8: in <module>
    from modules.patent.models import (
E   ImportError: cannot import name 'AuditLog' from 'modules.patent.models' (modules/patent/models.py)
_________________ ERROR collecting tests/a8/br/test_br_p10.py __________________
.venv/lib/python3.12/site-packages/_pytest/python.py:528: in importtestmodule
    mod = import_path(
.venv/lib/python3.12/site-packages/_pytest/pathlib.py:640: in import_path
    importlib.import_module(module_name)
/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
.venv/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:176: in exec_module
    source_hash, co = _rewrite_test(fn, self.config)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:341: in _rewrite_test
    co = compile(tree, strfn, "exec", dont_inherit=True)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E     File "tests/a8/br/test_br_p10.py", line 517
E       from tests.a8.br.test_br_p10 import *
E                                           ^
E   SyntaxError: import * only allowed at module level
Repair the TEST CODE/TEST SETUP only.
Do not modify production code.
Do not alter test intent or expected results.
Do not add or remove test cases.
Do not introduce new specification information.
Make only the minimum changes required to make the frozen tests executable.
