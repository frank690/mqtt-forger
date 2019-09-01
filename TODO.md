# NoveltyProducer - Todo

## not scheduled

- [ ] Update Documentation.
- [ ] Create an Visualizer class.
- [ ] Think about internal data flow and make changes if needed.

## version 0.1.x

### General

- [x] Add Documentation.
- [ ] 100% on unit tests.
- [x] Stop Scheduler when no generators are left in pipeline.

### Manager

- [x] Add functionality of adding/removing/changing generators.
- [x] Create function to update pipeline output.
- [x] Fully implement handling of multiple channels per pipeline.
- [x] Add dict with default values for parameters (frequencies, durations, etc...) and implement that.
- [x] `add_channel_to_pipeline`, `add_novelty_to_pipeline`: Add functionality.
- [x] `create_pipeline`: Only allow unique pipeline names.
- [x] `_add_handlers`: Fallback case on failed connection.
- [x] `switch_pipeline`: Adding further functionality.
    
### Generator

- [x] Add cyclic dead time.
- [x] Adding option of different kind of data output (currently just sin waves).

### Technican

- [x] Simplify Generator and Manager and introduce Technican instead.