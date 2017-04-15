import sys



class template_database(object):
    def __init__(self):
        pass

    def load_database(self,file_):
        t_database=open(file_,'r')
        lines=t_database.readlines()
        t_database.close()
        return lines
    def check_database(self,file_,ID):
        ID_string=str(ID)
        template=0
        lines=self.load_database(file_)
        for i in range(0,len(lines)):
            c_line=lines[i]
            if c_line[:7]==ID_string:
                template=c_line[8:]
                return template[:len(template)-1]#cut out the \n
        
        return template#return 0 ig the if ID was never found
    def write_template(self,file_,ID,template,overwrite=0):
        ID_string=str(ID)
        if self.check_database(file_,ID)==0:
            
            lines=self.load_database(file_)
            lines.append(str(ID)+','+template+'\n')
            t_database=open(file_,'w')
            for item in lines:
                t_database.write(item)
            t_database.close()
            return 1
        else:
            print('ID already exists')
            if overwrite:
                print('Overwrite enabled')
                lines=self.load_database(file_)

                t_database=open(file_,'w')
                for c_line in lines:
                    if c_line[:7]==ID_string:
                        c_line=str(ID)+','+template+'\n'
                    t_database.write(c_line)
                t_database.close()
            else:
                print('Overwrite disabled \nMost recent enroll for %d will be discarded' % ID)
            return 0
    def File_Write(self,file_,stringlist):
        file2write=open(file_,'w')
        #file2write.truncate()
        for line in stringlist:
            file2write.write(line+'\n')
        file2write.close()
    def File_Read(self,file_):
        return self.load_database(file_)

        
        




#t_database=open(filename,'r')

#temp_database=t_database.read()

#t_database.close()

#t_database=open(filename,'w')

#temp_database=temp_database+'2323232 , bye \n'

#t_database.write(temp_database)

#t_database.close()

