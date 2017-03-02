# python script to rip subject data from a sql database from the fossilfinder data
# NOTES
# raw data should have a reference_key that is clean - starting at 1 and incrementing by 1 for each row - not doing this will throw an error


import MySQLdb
conn = MySQLdb.connect("server","username","password","database")
c = conn.cursor()

# very unclean way of counting the number of rows in the raw data table to enable a while loop to count rows as it rips and parses each one
numrows = c.execute("select count(*) from raw_data")
rows = c.fetchall()
rows1 = list(rows[0])
numrows_raw_data = (rows1[0])

#this while loop takes one line at a time from the raw data table - code within parses the row and puts it into an existing table called click_data
while numrows_raw_data > 0:
  #  print (numrows_raw_data)
    numrows_raw_data_str = str(numrows_raw_data)
    #sql query to pull row from database
    numrows = c.execute("select subject_data from raw_data where reference_key= %s",(numrows_raw_data_str,))

    #turns output from query into useful form - a list
    rows = c.fetchall()
    rows1 = list(rows[0])
    rows1 = rows1[0]
    rows1 = rows1.decode('utf-8')
    #print (rows1)

    sub_id = rows1[2:]
    sub_id = sub_id[:sub_id.find("\"")]
    #print (sub_id)


    test1 = rows1.find("Filename")
    if test1 > 0:
        img_name = rows1[rows1.find("Filename")+11:]
        img_name = img_name[:img_name.find("\"")]
        date_time = ""
    else:
        img_name = rows1[rows1.find("Image_Name")+13:]
        img_name = img_name[:img_name.find("\"")]
        date = rows1[rows1.find("Date")+7:]
        date = date[:date.find("\"")]
        time = rows1[rows1.find("Time")+7:]
        time = time[:time.find("\"")]
        date = date.replace(":", "-")
        date_space = " "
        date_time = date+date_space+time
        
        
    
    


    c.execute("insert into subjects (subject_ids, image_name, taken_timestamp, reference_key) values (%s, %s, %s, NULL)",(sub_id, img_name, date_time))
    conn.commit()

    numrows_raw_data = numrows_raw_data - 1

#end of code
