"""This module holds information, data and more that is shared among tests."""

import numpy as np

sample_replay_data = [5 * np.tanh(x) for x in np.linspace(-2, 2, 10)]
generator_samples = [
    ("Foo", 1, "sin", 0, 0, None, None, None),
    ("Foo", 10.5, "rnd", 0, 0, None, None, None),
    ("Foo", 0.15, "fixed", 0, 0, None, None, None),
    ("Foo", 0.015, "replay", 0, 0, None, sample_replay_data, None),
    ("Bar", 1, "sin", 1, 1, None, None, None),
    ("Bar", 10.5, "rnd", 2, 0.5, None, None, None),
    ("Bar", 0.15, "fixed", 3, 0.2, None, None, None),
    ("Bar", 0.015, "replay", 4, 0.1, None, sample_replay_data, None),
    ("Baz", 1, "sin", 0, 0, [42, 1337], None, None),
    ("Baz", 10.5, "rnd", 0, 0, [-0.24, 0.99], None, None),
    ("Baz", 0.15, "fixed", 0, 0, [-8, -4], None, None),
    ("Baz", 0.015, "replay", 0, 0, [1, 2], sample_replay_data, None),
    ("Qux", 1, "sin", 1, 1, [0.1, 0.11], None, 2),
    ("Qux", 10.5, "rnd", 2, 0.5, [-10, 5], None, 3),
    ("Qux", 0.15, "fixed", 3, 0.2, [12.5, 14.81], None, 42),
    ("Qux", 0.015, "replay", 4, 0.1, None, sample_replay_data, 1337),
    ("Fail", 0.015, "wrong", 0, 0, None, None, 1337),
]
