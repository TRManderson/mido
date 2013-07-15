# -*- coding: utf-8 -*-

"""
MIDI Objects for Python

Mido is a library for working with MIDI messages and ports. It's
designed to be as straight forward and Pythonic as possible.

Creating messages:

    Message(type, **parameters) -- create a new message

Ports:

    open_input(name=None) -- open an input port
    open_output(name=None) -- open an output port
    open_ioport(name=None) -- open an I/O port (capable of both input
                                                and output)

    get_input_names() -- return a list of names of available input ports
    get_output_names() -- return a list of names of available output ports
    get_ioport_names() -- return a list of names of available I/O ports

Parsing MIDI streams:

    parse(bytes) -- parse a single message bytes
                    (any iterable that generates integers in 0..127)
    parse_all(bytes) -- parse all messages bytes
    Parser -- MIDI parser class

Parsing objects serialized with str(message):

    parse_string(string) -- parse a string containing a message
    parse_string_stream(iterable) -- parse strings from an iterable and
                                     generate messages

Sub modules:

    ports -- useful tools for working with ports

For more on MIDI, see:

    http://www.midi.org/


Getting started:

    >>> import mido
    >>> m = mido.Message('note_on', note=60, velocity=64)
    >>> m
    <note_on message channel=0, note=60, velocity=64, time=0>
    >>> m.type
    'note_on'
    >>> m.channel = 6
    >>> m.note = 19
    >>> m.copy(velocity=120)
    <note_on message channel=0, note=60, velocity=64, time=0>
    >>> s = mido.Message('sysex', data=[byte for byte in range(5)])
    >>> s.data
    (0, 1, 2, 3, 4)
    >>> s.hex()
    'F0 00 01 02 03 04 F7'
    >>> len(s)
    7

    >>> default_input = mido.open_input()
    >>> default_input.name
    'MPK mini MIDI 1'
    >>> output = mido.open_output('SD-20 Part A')
    >>>
    >>> for message in default_input:
    ...     output.send(message)

    >>> get_input_names()
    ['MPK mini MIDI 1', 'SH-201']
"""
from . import ports
from .messages import Message, parse_string, parse_string_stream
from .parser import Parser, parse, parse_all

__author__ = 'Ole Martin Bjørndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'http://github.com/olemb/mido/'
__license__ = 'MIT'
__version__ = '0.0.0'

# Prevent splat import.
__all__ = []


def get_input_names():
    """Return a sorted list of all input port names.
    These names can be passed to mido.open_input() and mido.open_output().
    """
    return _get_portmidi().get_input_names()


def get_output_names():
    """Return a sorted list of all output port names.
    These names can be passed to mido.open_input() and mido.open_output().
    """
    return _get_portmidi().get_output_names()


def get_ioport_names():
    """Return the names of all ports that allow input and output."""
    return sorted(set(get_input_names()) & set(get_output_names()))


def open_input(name=None):
    """Open an input port."""
    return _open_port(name, mode='i')


def open_output(name=None):
    """Open an output port."""
    return _open_port(name, mode='o')


def open_ioport(name=None):
    """Open a port for input and output."""
    return _open_port(name, mode='io')


def _get_portmidi():
    # Todo: check for exceptions?
    from . import portmidi
    return portmidi


def _open_port(name=None, mode=None, backend='portmidi'):
    backend = _get_portmidi()

    if mode == 'i':
        return backend.Input(name)
    elif mode == 'o':
        return backend.Output(name)
    elif mode == 'io':
        return ports.IOPort(backend.Input(name),
                            backend.Output(name))
    else:
        raise ValueError('invalid mode {!r}'.format(mode))
