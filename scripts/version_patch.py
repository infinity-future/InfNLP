#!/usr/bin/env python3


def main():
    version = open('version.txt', 'r').read().strip()
    a, b, c = [int(x) for x in version.split('.')]
    c += 1
    new_version = '{}.{}.{}'.format(a, b, c)
    with open('version.txt', 'w') as fp:
        fp.write(new_version)


if __name__ == '__main__':
    main()
