from secrets import choice
from xml.etree.ElementTree import tostring
import xlsxwriter
from data_input import *
from solver import buildDp, solve, uniqueGroups, mem, toPrint

to_print1 = []
to_print2 = []
to_print3 = []


def DISPLAY(branch_num, num_of_branches):
    for i in range(num_of_branches):
        print(f"\t\t\t{i + 1}. {branch_name[i]}")

    choice = branch_num
    # while choice.isnumeric() == False or int(choice) < 1 or int(choice) > num_of_branches:
    #    choice = input("Enter valid number: ")
    #choice = int(choice)

    solve(branch[choice - 1])

    print("\n\n\t\t >> valid options << \n")

    cnt = 1
    for group in uniqueGroups:
        print(f"{cnt}.")
        print("\tDay 1.   ", end=' ')
        for g in group[0]:
            print(g, end=' ')
        print()
        print("\tDay 2.   ", end=' ')
        for g in group[1]:
            print(g, end=' ')
        print()
        print("\tDay 3.   ", end=' ')
        for g in group[2]:
            print(g, end=' ')
        print()
        cnt += 1

    #choice2 = input("\nChoose Distribution: ")
    # while choice2.isnumeric() == False or int(choice2) < 1 or int(choice2) >= cnt:
    #    choice2 = input("Enter valid number: ")
    #choice2 = int(choice2)


def options(choice, choice2):
    print_output(choice - 1, choice2)


def print_output(choice1, choice2):
    cnt, R = 1, 2

    for group in uniqueGroups:
        if cnt < choice2:
            cnt += 1
            continue
        print("\n\n")
        mem.clear()
        buildDp(0, 0, group[0], branch[choice1].hallsInBranch)
        to_print1.extend(list(toPrint))
        print("\n")
        toPrint.clear()
        mem.clear()
        buildDp(0, 0, group[1], branch[choice1].hallsInBranch)
        to_print2.extend(list(toPrint))
        print("\n")
        toPrint.clear()
        mem.clear()
        buildDp(0, 0, group[2], branch[choice1].hallsInBranch)
        to_print3.extend(list(toPrint))
        print("\n")
        toPrint.clear()
        mem.clear()
        break


def output_the_distribution(choice1, choice2):
    choice1 -= 1
    workbook = xlsxwriter.Workbook('القاعات{}.xlsx'.format(choice2))
    worksheet = workbook.add_worksheet(branch_name[choice1])

    general_format = workbook.add_format()
    general_format.set_align('center')
    general_format.set_text_wrap()
    # general_format.set_border_color('black')

    header_format = workbook.add_format()
    # header_format.set_border_color('black')
    header_format.set_bg_color('red')
    header_format.set_align('center')
    header_format.set_font_size(20)
    header_format.set_text_wrap()
    header_format.set_bold()

    sub_header_format = workbook.add_format()
    # sub_header_format.set_border_color('black')
    sub_header_format.set_align('center')
    sub_header_format.set_bg_color('silver')
    sub_header_format.set_text_wrap()
    sub_header_format.set_font_size(16)

    del_format = workbook.add_format()
    del_format.set_diag_border()

    worksheet.set_column('A:J', 20)
    worksheet.set_column('C:D', 13)
    worksheet.set_column('F:G', 13)
    worksheet.set_column('I:J', 13)

    worksheet.right_to_left()

    worksheet.merge_range(0, 1, 0, 3, 'اليوم الاول', header_format)
    worksheet.merge_range(0, 4, 0, 6, 'اليوم الثاني', header_format)
    worksheet.merge_range(0, 7, 0, 9, 'اليوم الثالث', header_format)
    worksheet.write(1, 0, 'اسم القاعه', header_format)

    worksheet.write(1, 1, 'اسم الدفعه', sub_header_format)
    worksheet.write(1, 4, 'اسم الدفعه', sub_header_format)
    worksheet.write(1, 7, 'اسم الدفعه', sub_header_format)
    worksheet.write(1, 2, 'من', sub_header_format)
    worksheet.write(1, 5, 'من', sub_header_format)
    worksheet.write(1, 8, 'من', sub_header_format)
    worksheet.write(1, 3, 'الي', sub_header_format)
    worksheet.write(1, 6, 'الي', sub_header_format)
    worksheet.write(1, 9, 'الي', sub_header_format)

    cnt, R = 1, 2

    for group in uniqueGroups:
        if cnt < choice2:
            cnt += 1
            continue
        print("\n\n")
        mem.clear()
        buildDp(0, 0, group[0], branch[choice1].hallsInBranch)
        # to_print1.extend(list(toPrint))
        for i in range(len(toPrint)):
            worksheet.write(R + i, 0, toPrint[i][0], sub_header_format)
            worksheet.write(R + i, 1, toPrint[i][1], general_format)
            worksheet.write(R + i, 2, toPrint[i][2], general_format)
            worksheet.write(R + i, 3, toPrint[i][3], general_format)
        toPrint.clear()
        mem.clear()
        buildDp(0, 0, group[1], branch[choice1].hallsInBranch)
        # to_print2.extend(list(toPrint))

        for i in range(len(toPrint)):
            worksheet.write(R + i, 4, toPrint[i][1], general_format)
            worksheet.write(R + i, 5, toPrint[i][2], general_format)
            worksheet.write(R + i, 6, toPrint[i][3], general_format)
        toPrint.clear()
        mem.clear()
        buildDp(0, 0, group[2], branch[choice1].hallsInBranch)
        # to_print3.extend(list(toPrint))
        for i in range(len(toPrint)):
            worksheet.write(R + i, 7, toPrint[i][1], general_format)
            worksheet.write(R + i, 8, toPrint[i][2], general_format)
            worksheet.write(R + i, 9, toPrint[i][3], general_format)
        toPrint.clear()
        break

    workbook.close()
