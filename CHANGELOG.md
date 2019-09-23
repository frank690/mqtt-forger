# NoveltyProducer - Changelog

## 0.1.12 (2019-09-23)

* `get_data(...)` in NoveltyProducer/Generator.py input parameter is now optional.
* NoveltyProducer/Painter.py now also dynamically plots legend of each plot (channel name).

## 0.1.11 (2019-09-18)

* Modifications in NoveltyProducer/Generator.py.
    - Parameter limits_ and frequency_ are now optional.
    - New Parameter replay_data_ was added.
    - Added internal parameter replay_idx.
    - Adjusted `_check_input(...)` accordingly.
    - Data type 'replay' now valid.
    - Added 'replay' posibility to `get_data(...)`.
* Modifications in NoveltyProducer/Manager.py.
    - Changed default value for channel_limits to None.
    - Added default value for replay_data.
    - New function `add_replay(...)` to create channel with historic data.
        - Adjusted `_add_generator(...)` and `_add_channel(...)` accordingly.
    - Simplified `_add_handlers(...)`.
    
## 0.1.10 (2019-09-16)

* Minor bugfixes on test/test_manager.py.

## 0.1.9 (2019-09-15)

* Did some modifications on NoveltyProducer/Manager.py for simplyfication.
    - renamed several functions.
    - removed adding of channel from creating pipeline function.
    - adjusted tests/test_manager.py accordingly.

## 0.1.8 (2019-09-06)

* Updated TODO.md.
* Major modifications in NoveltyProducer/Painter.py.
    - Now displaying only last MEMORY seconds.
    - Channels are now added/deleted dynamically (depending on the incoming data stream).
    - Now catching the closing event of the window.

## 0.1.7 (2019-09-03)

* Updated TODO.md.
* Added first version of visualization tool (NoveltyProducer/Painter.py).

## 0.1.6 (2019-09-03)

* Modified test in test/test_manager.py.

## 0.1.5 (2019-09-03)

* Added new tests in test/test_manager.py and test/test_generator.py.

## 0.1.4 (2019-09-03)

* Bugfix in test/test_manager.py.

## 0.1.3 (2019-09-03)

* Bugfix in `_remove_generator` in NoveltyProducer/Manager.py.

## 0.1.2 (2019-09-03)

* Minor changes in NoveltyProducer/Manager.py.
    - `add_channel_to_pipeline` now returns channel id.
    - `create_pipeline` now returns pipeline id.
* Bugfixes in tests/test_manager.py.

## 0.1.1 (2019-09-03)

* Updated TODO.md.
* Bugfixes in tests/test_manager.py.

## 0.1.0 (2019-09-03)

* Added more unit tests.
* Minor modifications in NoveltyProducer/Generator.py.
    - Added VALID_TYPES in NoveltyProducer/Generator.py.
    - `_check_input` now also checking for valid types.
* `publish_data` in NoveltyProducer/Manager.py now returns mqtt status info.

## 0.0.40e (2019-09-02)

* Bugfixes in unit tests.

## 0.0.40d (2019-09-02)

* Bugfixes in unit tests.

## 0.0.40c (2019-09-02)

* Bugfixes in unit tests.

## 0.0.40b (2019-09-02)

* Bugfixes in unit tests.

## 0.0.40a (2019-09-02)

* Bugfixes in unit tests.

## 0.0.40 (2019-09-02)

* Bugfixes in unit tests.

## 0.0.39 (2019-09-02)

* Removed json from test-requirements.txt.

## 0.0.38 (2019-09-02)

* Reworked all unit tests.
* Made cdt_ input in `_seconds_since_init` in NoveltyProducer/Generator.py optional.
* Corrected typo in NoveltyProducer/Manager.py.
* Added error classes and `_check_input` function to NoveltyProducer/Technican.py.

## 0.0.37 (2019-09-01)

* Updated TODO.md.
* Modified NoveltyProducer/Manager.py.
    - Introduced channel types (sin, random and fixed).
    - Modified `_check_pipeline_materials` accordingly.
* Modified NoveltyProducer/Generator.py.
    - Introduced channel types (sin, random and fixed).

## 0.0.36a (2019-08-31)

* Merging issue.

## 0.0.36 (2019-08-30)

* Major changes in NoveltyProducer/Manager.py.
    - Added several functions to handle dynamic adding/removing of generators.
    - Removed noise and all its related parameters/functions.
    - pipelines are now automatically switched on/off if any/no channels are assigned to it.
* Major changes in NoveltyProducer/Generator.py.
    - Removed noise and all its related parameters/functions.
    - Added possibility of cyclic deadtime.
* Updated TODO.md.
* Added json to test-requirements.txt.
* Added NoveltyProducer/Technican.py.

## 0.0.35 (2019-08-29)

* Bugfix in NoveltyProducer/Manager.py.

## 0.0.34 (2019-08-29)

* Added default values as dict in NoveltyProducer/Manager.py.
* Updated TODO.md.

## 0.0.33 (2019-08-29)

* Bugfix in tests/test_manager.py.

## 0.0.32 (2019-08-29)

* Bugfix in tests/test_manager.py.

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