@python -m coverage erase
@FOR %%I in (.\tests\test_*.py) DO  python -m coverage run --source reversi %%I
@python -m coverage report
@pause