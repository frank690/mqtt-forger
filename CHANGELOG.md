# NoveltyProducer - Changelog

## 0.0.21 (2019-08-27)

* Adding missing import of custom exception classes in tests/test_manager.py.

## 0.0.20 (2019-08-27)

* Here we go again... Bugfix in tests/test_manager.py.

## 0.0.19 (2019-08-27)

* Expanded tests/test_manager.py.
* Modified NoveltyProducer/Manager.py.
    - Added `InvalidInputTypeError(Exception)` and `InvalidInputValueError(Exception)` as exception classes.
    - Added `_check_pipeline_materials(...)`.
        - Modified `create_pipeline(...)` accordingly.
        
## 0.0.18 (2019-08-27)

* Added `paho-mqtt` to test-requirements.txt.

## 0.0.17 (2019-08-27)

* Added `apscheduler` to test-requirements.txt.

## 0.0.16 (2019-08-27)

* Added tests/test_manager.py.
* Added further testing in tests/test_generator.py.
* Renamed main class in NoveltyProducer/Manager.py from NoveltyProducer to Manager.

## 0.0.15 (2019-08-27)

* Removed copy and deepcopy comparsion in `test_type_output(...)` in tests/test_generator.py.

## 0.0.14 (2019-08-27)

* Bugfix in test/test_generator.py.

## 0.0.13 (2019-08-27)

* Bugfix in test/test_generator.py.

## 0.0.12 (2019-08-27)

* Today is fixing day in test/test_generator.py.

## 0.0.11 (2019-08-27)

* You know how we do. Bugfix in test/test_generator.py.

## 0.0.10 (2019-08-27)

* Yet another bugfix in test/test_generator.py.

## 0.0.9 (2019-08-27)

* Bugfix in test/test_generator.py.

## 0.0.8 (2019-08-27)

* Removed __init__.py from main folder.
* Removed content from __init__.py from NoveltyProducer folder.

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