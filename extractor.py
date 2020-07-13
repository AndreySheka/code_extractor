#!/usr/bin/env python
import os
import fnmatch
import glob
from argparse import ArgumentParser, ArgumentTypeError

def check_dest(dest):
    if not os.path.exists(dest) or not os.path.isdir(dest):
            msg = "%r directory is not exist" % dest
            raise ArgumentTypeError(msg)        
    return dest

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--destination", dest="dest", required=True, 
                        type=check_dest, 
                        help="destination directory for code extractor")
    parser.add_argument("-m", "--mask", dest="mask", default="*?.*", 
                        type=lambda s: s.split(','),
                        help="file mask for code extractor")
    parser.add_argument("-o", "--output", dest="out", default="output.txt" ,
                        help="output file for code extractor")
                        
    args = parser.parse_args()

    files = []
    for m in args.mask:
        m = os.path.join(args.dest, "**", m)
        files += glob.glob(m, recursive=True)

    print("Extracted files:")
    for name in files:
        print(name)
        
    print("Total files: %i" % len(files))
    with open(args.out, "w", encoding='utf-8', errors='ignore') as out:
        for f in files:
            print("file: %s" % f[len(args.dest) + 1:], file=out)
            with open(f, "r", encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if len(line.strip()):
                        print(line, file=out, end='')
            print(file=out)
