import argparse
import numpy as np
from jinja2 import Environment, FileSystemLoader
from subprocess import Popen


OPTIONAL_ROWS = 3


def find_unbroken_lines(s):
    res = []
    cnt = 0
    for val in s:
        if val:
            cnt += 1
        elif cnt:
            res.append(str(cnt))
            cnt = 0
    if cnt:
        res.append(str(cnt))
    return res or ['0']


def draw_thick(i, square_side, max_x, h):
    first = max_x % square_side
    return (i + 1) % square_side == first or i + 1 == h


def stringify(s):
    return "" if s is None else "$\\!$" + s


def print_tex(m, max_x, max_y, square_side, out_pref, pdf):
    h, w = m.shape
    rows = [" & ".join(map(stringify, row)) + r" \\ \tabucline" +
            ("[3pt]" if draw_thick(i, square_side, max_x, h) else "")
            + "{1-%d}" % w for i, row in enumerate(m)]
    first = max_y % square_side
    block_sep = "K{6mm}|"
    blocks = [block_sep * first] if first else []
    blocks += [block_sep * square_side] * ((w - first) // square_side)
    if (w - first) % square_side:
        blocks += [block_sep * ((w - first) % square_side)]
    preamble = "|[3pt]{}[3pt]".format("[3pt]".join(blocks))
    env = Environment(loader=FileSystemLoader(''))
    template = env.get_template("template.tex")
    with open(out_pref + '.tex', 'w') as f:
        f.write(template.render(preamble=preamble, width=w, rows=rows))
    if pdf:
        Popen(['pdflatex', out_pref + '.tex'])


def make_matrix(cnt_x, cnt_y, max_x, max_y, h, w):
    m = np.empty([h + max_x, w + max_y], dtype=object)
    for i, arr in enumerate(cnt_y):
        m[max_x + i][max_y - len(arr):max_y] = arr
    for i, arr in enumerate(cnt_x):
        m.T[max_y + i][max_x - len(arr):max_x] = arr
    return m


def main():
    parser = argparse.ArgumentParser(description="a tool used to generate nonogram by picture")
    parser.add_argument('i', type=argparse.FileType('r'), help="input file in .pbm format")
    parser.add_argument('-o', type=str, nargs='?',
                        help="output prefix", default="out")
    parser.add_argument('-s', type=int, nargs='?', help='square side', default=5)
    parser.add_argument('-pdf', help="make pdf using pdflatex tool", dest='pdf', action='store_true')
    parser.set_defaults(pdf=False)
    args = parser.parse_args()
    img = np.loadtxt(args.i, skiprows=OPTIONAL_ROWS)
    cnt_y = [find_unbroken_lines(line) for line in img]
    cnt_x = [find_unbroken_lines(line) for line in img.T]
    max_x = max(len(lst) for lst in cnt_x)
    max_y = max(len(lst) for lst in cnt_y)
    m = make_matrix(cnt_x, cnt_y, max_x, max_y, *img.shape)
    print_tex(m, max_x, max_y, args.s, args.o, args.pdf)


if __name__ == '__main__':
    main()
