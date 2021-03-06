# python script to rip click data from a sql database from the fossilfinder data
# NOTES
# raw data should have a reference_key that is clean - starting at 1 and incrementing by 1 for each row - not doing this will throw an error
# this code rips T3 from the data - so clicks are for individual object ids of interest
# tested as working on a table with three rows at present


import MySQLdb
conn = MySQLdb.connect("server-name-here","user-name-here","password-here","database-name-here")
c = conn.cursor()

# very unclean way of counting the number of rows in the raw data table to enable a while loop to count rows as it rips and parses each one
numrows = c.execute("select count(*) from raw_data")
rows = c.fetchall()
rows1 = list(rows[0])
numrows_raw_data = (rows1[0])

#this while loop takes one line at a time from the raw data table - code within parses the row and puts it into an existing table called click_data
while numrows_raw_data > 0:
    print (numrows_raw_data)
    numrows_raw_data_str = str(numrows_raw_data)
    #sql query to pull row from database
    numrows = c.execute("select classification_id, annotations, user_name, subject_ids, workflow_id, workflow_version, created_at from raw_data where reference_key= %s",(numrows_raw_data_str,))

    #turns output from query into useful form - a list
    rows = c.fetchall()
    rows1 = list(rows[0])

    #puts one entry from table into a variable
    var1 = rows1[1]

    #finds start of tool 3 content and rips it off the variable
    front1 = var1.find(b"T3")
    var1 = var1[front1:]
   
    #finds start of datastring and crops to bracket
    front1 = var1.find(b"{")
    var1 = var1[front1:]

    #removes end of datastring to bracket WARNING THAT THIS COULD VARY
    front1 = len(var1)-3
    var1 = var1[:front1]
   
    while len(var1) > 5:
    #    var1_x = var1[:var1.find(b"\"\"}")+2]

        #extracting x coord
        var1_1 = var1[var1.find(b"x")+3:]
        var1_1 = var1_1[:(var1_1.find(b","))]
        #pt = var1_1.find(b"null")
        #print (pt)
        if var1_1.find(b"null") == 0:
            var1_1 = 0.0
        
        #extracting y coord
        var1_2 = var1[var1.find(b"y")+3:]
        var1_2 = var1_2[:(var1_2.find(b","))]
        
        if var1_2.find(b"null") == 0:
            var1_2 = 0.0

        #extracting tool label
        var1_3 = var1[var1.find(b"tool_label")+13:]
        var1_3 = var1_3[:var1_3.find(b"\"")]

        c.execute("INSERT INTO click_data_t3 (classification_id, x_coord, y_coord, label, user_name, subject_ids, workflow_id, workflow_version, created_at, reference_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)",(rows1[0], var1_1, var1_2, var1_3, rows1[2], rows1[3], rows1[4], rows1[5], rows1[6]))
        conn.commit()

        var1 = var1[var1.find(b"\"}")+2:]
    numrows_raw_data = numrows_raw_data - 1

#end of code
