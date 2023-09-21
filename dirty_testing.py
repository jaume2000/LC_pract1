import sys
sys.path.append('../')

from utils.math_lines import Line
format = "{:<10} {:<22} {:<22} {:<10} {:<10}"
i=0

def test(l1,l2, expected):
    global i
    got = l1.intersect_lines(l2)
    print(format.format(i, str(l1.p1) + "->" + str(l1.p2), str(l2.p1) + "->" + str(l2.p2), str(got), str(got == expected)))
    i+=1


print(format.format("Test", "Line 1", "Line 2", "Got", "Passed Test"))




test(Line(27,25,30,38), Line(30,0,30,70), True)