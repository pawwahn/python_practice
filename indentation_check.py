try:
    parent.info(" current working directory1 :{}".format(os.getcwd()))
    change_directory_path = os.chdir(member_number_path)
    parent.info(change_directory_path)
    parent.info(" current working directory2 :{}".format(change_directory_path)
    member_numbers ='40447'
    parent.info(member_numbers)
    mem_num_file = str(member_number)+'_response.txt'
    parent.info(mem_num_file)
    f = open(mem_num_file, "a")
    f.write(output_xml)
    f.close()
except e:
    parent.info("file not found or other exception")