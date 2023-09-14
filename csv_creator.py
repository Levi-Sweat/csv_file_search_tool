import csv

class Data:
    zero_min = ''
    one_min = ''
    two_min = ''
    three_min = ''
    four_min = ''

    def __init__(self, filename, offset, species):
        self.filename = filename
        self.offset = offset
        self.species = species

    def set_offset(self, new_offset):
        self.offset = new_offset

    def label_offset(self):
        self.offset = int(self.offset / 60)
        if self.offset == 0:
            self.zero_min = 'X'
        elif self.offset == 1:
            self.one_min = 'X'
        elif self.offset == 2:
            self.two_min = 'X'
        elif self.offset == 3:
            self.three_min = 'X'
        elif self.offset == 4:
            self.four_min = 'X'

    def create_data_row(self):
        new_row_array = []

        filename = self.filename
        first_columns = filename.split("_")

        new_row_array.append(first_columns[0])
        new_row_array.append(first_columns[1])
        new_row_array.append(first_columns[2])

        new_row_array[2] = new_row_array[2][:-4]

        new_row_array.append('')
        new_row_array.append('')
        new_row_array.append(self.species)
        new_row_array.append('')
        new_row_array.append(self.zero_min)
        new_row_array.append(self.one_min)
        new_row_array.append(self.two_min)
        new_row_array.append(self.three_min)
        new_row_array.append(self.four_min)
        new_row_array.append('')
        new_row_array.append('')
        new_row_array.append('')
        new_row_array.append('')
        new_row_array.append('')

        return new_row_array


species_input = input("Which species/cluster are you searching for?\n") #Where program starts, user input for species/cluster name

#header of the new_cluster.csv output file
header = ["Full name", "Unit", "File Name Y/M/D", "File Time", "Initials", "Date", "Species", "No. Ind.", "Second/Offset Detected", "TMTC", "VT", "TBC", "Comment", "Verified"]

#header of the final_cluster.csv output file
final_header = ["Unit", "File Name Y/M/D", "File Time", "Initials", "Date", "Species", "No. Ind.", "0min", "1min", "2min", "3min", "4min", "TMTC", "VT", "TBC", "Comment", "Verified"]


with open('new_cluster.csv', 'w', newline='') as new_file:
    csv_writer = csv.writer(new_file)
    csv_writer.writerow(header)

    with open('cluster.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            if line[15] == species_input:
                filename = line[2]

                row_array = filename.split("_")
                
                row_array[2] = row_array[2][:-4]    # remove the .wav extension from the times of the detections

                row_array.insert(0, filename)       # insert filename to the beginning of list

                row_array.append('')
                row_array.append('')
                row_array.append(line[15])
                row_array.append('')
                row_array.append(line[4])
                row_array.append('')
                row_array.append('')
                row_array.append('')
                row_array.append('')
                row_array.append('')
                    
                csv_writer.writerow(row_array)


file_name_objects = []

with open('final_cluster.csv', 'w', newline='') as final_csv:
    csv_writer = csv.writer(final_csv)
    csv_writer.writerow(final_header)

    with open('new_cluster.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        x = True
        
        while x:
            row = next(csv_reader)                              # skip header
            row = next(csv_reader)                              # look at first data row

            while row[0] in file_name_objects:                  # Checks if filename object has already been created
                try:
                    row = next(csv_reader)                      # Tries to look at next CSV line, if it can't breaks out of loop as the file is finished
                except StopIteration:
                    x = False
                    break

            if row[0] not in file_name_objects:               
                data = Data(row[0], float(row[8]), row[6])      # create object based on the contents
                file_name_objects.append(data.filename)         # add filename to list to skip over in the next iterations
                data.label_offset()                             # label data sheet based on the time the detection happens
                
                try:
                    row = next(csv_reader)                      # move to the next line if possible
                except StopIteration:
                    break

                while row != None:                              # while the row is not empty
                    if row[0] == data.filename:                 # if the filename of the next row matches the current data object:
                        data.set_offset(float(row[8]))
                        data.label_offset()                     # label the detection on the datasheet
                        try:
                            row = next(csv_reader)
                        except StopIteration:
                            row = None                          # break out of loop if at the end of the file
                    else:
                        try:
                            row = next(csv_reader)
                        except StopIteration:
                            row = None
                    
                csv_writer.writerow(data.create_data_row())     # write to the datasheet

                csv_file.seek(0)                                # return to the beginning of file