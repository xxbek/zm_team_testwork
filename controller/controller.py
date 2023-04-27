import argparse


def parse_args() -> argparse.Namespace:
    """Parser for command-line options"""
    parser = argparse.ArgumentParser(description='User interaction tool.')

    parser.add_argument(
        'setting_path',
        metavar='<SETTING PATH>',
        type=str,
        help='set path to your setting',
    )

    return parser.parse_args()
