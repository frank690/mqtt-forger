# NoveltyProducer - Changelog

## 0.0.7 (2019-08-27)

* Added .gitignore file.
* Added __init__.py in NoveltyProducer.

## 0.0.6 (2019-08-27)

* Renamed NoveltyProducer.py to Manager.py.
* Bugfix in test/test_generator.py.

## 0.0.5 (2019-08-27)

* Moved Generator.py and NoveltyProducer.py in NoveltyProducer subfolder.

## 0.0.4 (2019-08-27)

 * Bugfix in test/test_generator.py.

## 0.0.3 (2019-08-27)

* Bugfix in .travis.yml.

## 0.0.2 (2019-08-27)

* Added .travis.yml, tests/test_generator.py, test-requirements.txt and setup.py.
* Major changes in Generator.py:
    - Added several Exception classes.
    - Added optional input seed for random number generator.
    - Added `_check_input` to check given inputs.
    - Modified `_get_noise` and `get_data` to work with optional times_ input.
    - Modified `get_payload` and `_get_times` accordingly.
    - Added `_plant_a_seed` to (re)plant seed into random number generator.
* Fixed typo in NoveltyProducer.py.

## 0.0.1 (2018-08-22)

* Added CHANGELOG.md.
* Bugfix on NoveltyProducer.py.