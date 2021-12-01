#!/usr/bin/env python3
import argparse
import os, sys
from importlib import import_module
import pathlib
from orrinjelo.utils.fileio import load_file

current_path = os.path.split(os.path.realpath(__file__))[0]
this_dir = pathlib.PurePath(current_path).name 

def main():
    parser = argparse.ArgumentParser(description='AOC entry point')
    parser.add_argument('problem_number', type=int, nargs=1,
                        help='problem number to run')
    parser.add_argument('--input_file', dest='input_file', type=str, default=None,
                        help='input file')
    parser.add_argument('--input', dest='input', type=str, default=None,
                        help='input string')
    parser.add_argument('--plot', action='store_true', default=None,
                        help='plot, if available')

    args = parser.parse_args()

    problem_number = str(args.problem_number[0]).zfill(2)
    input_file = args.input_file if args.input_file is not None else os.path.join(current_path, '..', 'inputs', f'day_{problem_number}.txt')
    input_str = args.input
    if input_str is None:
        try:
            input_ = load_file(input_file)
        except FileNotFoundError:
            print('Cannot find input file.  Supply one with --input_file, or a string with --input.')
            sys.exit(1)
        if len(input_) == 1:
            input_ = input_[0]
    else:
        input_ = input_str

    print('Input:', input_file if input_str is None else input_str)
    print('Day:', problem_number)
    
    try:
        mod = import_module(f'orrinjelo.aoc2021.day_{problem_number}')
    except ModuleNotFoundError:
        print(f'{problem_number} not found.')
        sys.exit(1)

    print('Part 1 result:', mod.part1(input_))
    print('Part 2 result:', mod.part2(input_))

    if args.plot:
        mod.plot(input_)

if __name__ == '__main__':
    main()