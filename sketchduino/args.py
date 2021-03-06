# -*- coding: utf-8 -*-
'''
Copyright 2012 Rodrigo Pinheiro Matias <rodrigopmatias@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from argparse import ArgumentParser


def parse_args():
    parse = ArgumentParser(description='The Arduino Sketch utiliter')

    parse.add_argument(
        '--processor',
        dest='mcu',
        help='The name of Microcontroler Unit.'
    )

    parse.add_argument(
        '--clock',
        dest='clock',
        help='The clock of Microcontroler Unit in MHz.',
        type=float
    )

    parse.add_argument(
        '--sdk',
        dest='sdk_home',
        help='The path for SDK of arduino.'
    )

    parse.add_argument(
        '--avr',
        dest='avr_home',
        help='The path for AVR/GNU compiler.'
    )

    parse.add_argument(
        '--cmd',
        dest='command',
        help='The command for Sketch utility.',
        required=True
    )

    parse.add_argument(
        '--project',
        dest='project_home',
        help='The home directory for project.',
        default=''
    )

    parse.add_argument(
        '--programer',
        dest='programer',
        help='The programer hardware for deploy you firmwire.',
    )

    parse.add_argument(
        '--serial',
        dest='serial',
        help='The serial port for comunication with hardware.',
    )

    parse.add_argument(
        '--baudrate',
        dest='baudrate',
        default=None,
        help='The serial baudrate for comunication with hardware.',
    )

    parse.add_argument(
        '--variant',
        dest='variant',
        help='The variante of your arduino.'
    )

    return parse.parse_args().__dict__
