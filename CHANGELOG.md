# NoveltyProducer - Changelog

## 0.0.31 (2019-08-29)

* Rearranged contents of `test_value_output(...)` to `test_type_output(...)` in tests/test_manager.py.

## 0.0.30 (2019-08-29)

* Updated TODO.md.
* Modifications in NoveltyProducer/Manager.py.
    - Added `OnConnectError(Exception)` class.
    - Added try/catch on client connection in `_add_handlers(...)`.
    - Jobs are now paused/resumed when `switch_pipeline(...)` is used.

## 0.0.29 (2019-08-29)

* Updated TODO.md.
* Modifications in NoveltyProducer/Manager.py.
    - Renamed `add_novelty_to_channel(...)` to `add_novelty_to_pipeline(...)`.
    - Added functionality to `add_channel_to_pipeline(...)` and `add_novelty_to_pipeline(...)`.
    - Modified `_add_pipeline(...)` to make sure that pipeline names are unique.
        - Added `_get_unique_name(...)` and `_count_up(...)`.
* Adjusted test-requirements.txt since re lib is now used in NoveltyProducer/Manager.py.

## 0.0.28 (2019-08-28)

* Renamed docs/README.rst to docs/index.rst.

## 0.0.27 (2019-08-28)

* Introduced documentation.
* Modified TODO.md.
* Added -yet empty- `add_channel_to_pipeline(...)` and `add_novelty_to_channel(...)` to NoveltyProducer/Manager.py.

## 0.0.26 (2019-08-28)

* Fixed the bugfix in `test_type_output(...)` in tests/test_manager.py.

## 0.0.25 (2019-08-28)

* Bugfix in `test_type_output(...)` in tests/test_manager.py.

## 0.0.24 (2019-08-28)

* Minor modifications in tests/test_manager.py:
    - changed from localhost to external mqtt broker.
    - bugfix in `test_value_output(...)`.

## 0.0.23 (2019-08-28)

* Added TODO.md.
* Expanded tests/test_manager.py.
* Minor modifications in NoveltyProducer/Manager.py.
    - Now default pipeline name is 'Pipe'.
    - Pipeline id is now passed as job id in scheduler.
    
## 0.0.22 (2019-08-27)

* Bugfix in `test_type_output(...)` in tests/test_manager.py.

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