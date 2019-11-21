import os
print (os.getcwd())
os.chdir("Q:\songs\Songs_new\pk")

for file in os.listdir("Q:\songs\Songs_new\pk1"):
    file_name , file_ext = os.path.splitext(file)
    print (file_name + " --> "+ file_ext)
    #print file_name.split('-')
    song_no, default_address, song_name = file_name.split('-')
    print (song_no,default_address,song_name)
    song_waste, new_song_no, song_waste_space = song_no.split(' ')
    print (new_song_no.strip(),song_name.strip(),file_ext)
    #new_file_names = '{}-{}{}'.format(new_song_no.strip().zfill(3), song_name.strip(), file_ext)
    #print new_file_names
    #os.rename(file,new_file_names)