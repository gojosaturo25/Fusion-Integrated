The generated test suite cannot execute because of the following test-code/setup error:
==================================== ERRORS ====================================
_________________ ERROR collecting tests/a8/fr/test_fr_p06.py __________________
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
.venv/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:339: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/ast.py:52: in parse
    return compile(source, filename, mode, flags,
E     File "tests/a8/fr/test_fr_p06.py", line 151
E       def test_test_id_TEST-CFR-008-4_source_id_PMS-AFR-070_restart_review_cycle_after_resubmission(
E                                 ^^
E   SyntaxError: leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers
_________________ ERROR collecting tests/a8/fr/test_fr_p11.py __________________
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
.venv/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:339: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/ast.py:52: in parse
    return compile(source, filename, mode, flags,
E     File "tests/a8/fr/test_fr_p11.py", line 127
E       self.source_id = "PMS-AFR-110"
E   IndentationError: unexpected indent
Repair the TEST CODE/TEST SETUP only.
Do not modify production code.
Do not alter test intent or expected results.
Do not add or remove test cases.
Do not introduce new specification information.
Make only the minimum changes required to make the frozen tests executable.
