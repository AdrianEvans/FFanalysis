# quick and dirty code to plot user clicks labelled by tool

import matplotlib.pyplot as plt
import MySQLdb

# database connection
conn = MySQLdb.connect("localhost","username","password","fossilfinder")
c = conn.cursor()

# basic way to select a subject - obviously could be looped through a database if we wanted to produce a chart for all things
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

# changes each text label to a particular colour - could be replaced by adding columns in a database for speed
# note there are probably entries to add here since the text used for tool 3 across the data with workflow changes
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

#changes each text label to a particular marker style - could be replaced by adding columns in a database for speed
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


#runs through the data and plots each point
for mar, col, lab, _x, _y in zip(marker_shape, marker_colour, l, x, y):
    plt.scatter(_x, _y, label=lab, c=col, marker=mar, alpha=.5)

# sets the axis based on image pixel size for our subjects
plt.axis([0.0,795,0.0,545])

# this allows the background image to be set as a subject
# currently just for demo. needs to be linked to an image folder with all the subjects and then to the subject_of_interest variable
im = plt.imread("940440.png")
implot = plt.imshow(im)

ax = plt.gca()
ax.set_autoscale_on(False)
ax.invert_yaxis()
ax.set_aspect('equal')

# this code is trying to remove as much of the image around the frame as possible. Still not quite there.
#Tempted to produce eps files from scratch and ditch pyplot. but i'm sure there is a way
ax.axis('off')
ax.set_frame_on(False)
plt.tight_layout()
#ax.legend()

# for window display of graph
#plt.xlabel('x')
#plt.ylabel('y')
#plt.title(subject_of_interest)
#plt.show()

#rather than produce a plot in a window this does a nice job of outputting an eps file that can be used
file_name = str(subject_of_interest) + "_clicks.eps"
plt.savefig(file_name, bbox_inches=0, pad_inches=0)
