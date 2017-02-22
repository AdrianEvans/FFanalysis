# quick and dirty code to plot user clicks labelled by tool

import matplotlib.pyplot as plt
import MySQLdb

#database connection
conn = MySQLdb.connect("localhost","adrianevans","CJ3ByCTc!","fossilfinder")
c = conn.cursor()

subject_of_interest = 940440

#extracts x y and labels into rows
c.execute("select x_coord from click_data_t3 where subject_ids = %s",(subject_of_interest,))
x = list(c.fetchall())
c.execute("select y_coord from click_data_t3 where subject_ids = %s",(subject_of_interest,))
y = list(c.fetchall())
c.execute("select label from click_data_t3 where subject_ids = %s",(subject_of_interest,))
l = list(c.fetchall())
marker_colour = []
marker_shape = []
for i in l:
    if ("%s" % i) == "may be something":
        i = "red"
    if ("%s" % i) == "Fossil Bone/Tooth":
        i = "blue"
    if ("%s" % i) == "Root-Cast/Rhizolith":
        i = "green"
    if ("%s" % i) == "Fossil Shell/Snails":
        i = "orange"
    if ("%s" % i) == "Stromatolite":
        i = "black"
    if ("%s" % i) == "stone tool":
        i = "purple"
    marker_colour.append(i)

for i in l:
    if ("%s" % i) == "may be something":
        i = 's'
    if ("%s" % i) == "Fossil Bone/Tooth":
        i = 'o'
    if ("%s" % i) == "Root-Cast/Rhizolith":
        i = '^'
    if ("%s" % i) == "Fossil Shell/Snails":
        i = "*"
    if ("%s" % i) == "Stromatolite":
        i = "v"
    if ("%s" % i) == "stone tool":
        i = "<"
    marker_shape.append(i)

#print (marker_shape[0])



for mar, col, lab, _x, _y in zip(marker_shape, marker_colour, l, x, y):
    plt.scatter(_x, _y, label=lab, c=col, marker=mar, alpha=.5)
    
plt.axis([0.0,795,0.0,545])
im = plt.imread("940440.png")
implot = plt.imshow(im)
ax = plt.gca()
ax.set_autoscale_on(False)
ax.invert_yaxis()
ax.set_aspect('equal')
ax.axis('off')
ax.set_frame_on(False)
plt.tight_layout()
#ax.legend()

#plt.xlabel('x')
#plt.ylabel('y')
#plt.title(subject_of_interest)
#plt.show()


file_name = str(subject_of_interest) + "_clicks.eps"
plt.savefig(file_name, bbox_inches=0, pad_inches=0)
