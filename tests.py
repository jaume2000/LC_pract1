from problem import Line
format = "{:<10} {:<22} {:<22} {:<10} {:<10}"
i=0

def test(l1,l2, expected):
    global i
    got = l1.intersect_lines(l2)
    print(format.format(i, str(l1.p1) + "->" + str(l1.p2), str(l2.p1) + "->" + str(l2.p2), str(got), str(got == expected)))
    i+=1


print(format.format("Test", "Line 1", "Line 2", "Got", "Passed Test"))


#True General Case
test(Line(4,4,0,0), Line(4,0,0,4), True)
test(Line(0,0,4,4), Line(4,0,0,4), True)
test(Line(0,0,4,4), Line(0,4,4,0), True)
test(Line(4,4,0,0), Line(0,4,4,0), True)

#Extreme General Case
test(Line(4,4,2,2), Line(0,4,4,0), True)
test(Line(4,4,2.01,2.01), Line(0,4,4,0), False)
test(Line(-1,-1,1,1), Line(-2,-2,2,2), True)
test(Line(-1,-1,1,1), Line(0,0,2,2), True)
test(Line(-1,-1,1,1), Line(2,2,1,1), True)
test(Line(-1,-1,1,1), Line(1.01,1,2,2), False)

#False General Case
test(Line(-1,-1,1,1), Line(-2,-1,0,1), False)
test(Line(1,1,0,0), Line(1,0,2,1), False)

#Horizontal intersections
test(Line(1,0,0,0), Line(0.5,0,5,0), True)
test(Line(0,1,0,0), Line(7,0,1,0), False)
test(Line(0,1,0,0), Line(7,0,0.5,0), False)
test(Line(10,0,-2,0), Line(3,0,4,0), True)
test(Line(1,0,-2,0), Line(3,0,4,0), False)

#One is horizontal, other not
test(Line(0,2,10,2), Line(0,2,2,3), True)
test(Line(0,2,10,2), Line(0,1,2,3), True)
test(Line(0,2,10,2), Line(0,2.1,2,3), False)
test(Line(0,2,10,2), Line(-2,0,1,3), True)
test(Line(0,2,10,2), Line(-3.1,0,1,3), False)

#Vertical lines
test(Line(-3,1,-3,2), Line(-3,1,-3,0), True)
test(Line(-3,1,-3,2), Line(-3,5,-3,2), True)
test(Line(-3,1,-3,2), Line(-3,5,-3,2.1), False)
test(Line(-3,1,-3,2), Line(-2,5,-2,2.1), False)
test(Line(-3,1,-3,2), Line(-2,5,-2,1.5), False)
test(Line(-3,1,-3,2), Line(-2,1.5,-2,0), False)
test(Line(-3,1,-3,2), Line(-2,3,-2,0), False)

test(Line(-3,1,-3,2), Line(-3,5,-3,1.5), True)
test(Line(-3,1,-3,2), Line(-3,1.5,-3,0), True)
test(Line(-3,1,-3,2), Line(-3,3,-3,0), True)
