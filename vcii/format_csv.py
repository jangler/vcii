import csv

from vcii.sheet import Sheet


def read(filename):
    with open(filename, newline='') as f:
        try:
            dialect = csv.Sniffer().sniff(f.read())
        except:
            dialect = csv.excel
        f.seek(0)
        reader = csv.reader(f, dialect)
        sheet = Sheet()
        sheet.title = filename
        for row in reader:
            sheet.cursor[0] = 0
            for cell in row:
                sheet.append(cell)
                sheet.cursor[0] += 1
            sheet.cursor[1] += 1
        for column in range(sheet.size[0]):
            width = max(len(sheet.cells[column][row].content)
                        for row in range(sheet.size[1])) + 1
            sheet.column_widths[column] = width
        sheet.cursor = [0, 0]
        sheet.modified = False
        sheet.status = 'Read file'
        return sheet


def write(sheet, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in range(sheet.size[1]):
            writer.writerow([sheet.cells[column][row].content
                             for column in range(sheet.size[0])])
        sheet.title = filename
        sheet.modified = False
        sheet.status = 'Wrote file'
