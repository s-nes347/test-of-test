import ftplib

def file_path(word):
    
    dir_name = "/{}{}".format(word[0], "0"*(len(word)-1))
    pdf_list = []
    web_address = "test9test.html.xdomain.jp"
    
    ftp = ftplib.FTP("sv2.html.xdomain.ne.jp")
    ftp.set_pasv('true')
    ftp.login(web_address, "pass0347")
    ftp.cwd(dir_name)
    file_list = ftp.nlst(".")
    for pdf_path in file_list:
        if pdf_path in word:
            pdf_list.append(web_address + dir_name + "/" + pdf_path)
    return pdf_list
            