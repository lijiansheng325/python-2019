import xml.etree.ElementTree as ET
import xlwt
import sys

def cts_result_parser(cts_xml_file_name, parser_result_excel_file_name):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('CTS testing results')

    pattern = xlwt.Pattern() 
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN 
    pattern.pattern_fore_colour = 23
    style = xlwt.XFStyle() 
    style.pattern = pattern

    pattern2 = xlwt.Pattern() 
    pattern2.pattern = xlwt.Pattern.SOLID_PATTERN 
    pattern2.pattern_fore_colour = 22
    style2 = xlwt.XFStyle()
    style2.pattern = pattern2

    pattern3 = xlwt.Pattern() 
    pattern3.pattern = xlwt.Pattern.SOLID_PATTERN 
    pattern3.pattern_fore_colour = 16
    style3 = xlwt.XFStyle() 
    style3.pattern = pattern3

    worksheet.write(0, 0, 'packages')
    worksheet.write(0, 1, 'cases')
    worksheet.write(0, 2, 'test')
    worksheet.write(0, 3, 'result')
    worksheet.write(0, 4, 'fail_scene')
    worksheet.write(0, 5, 'stack_trace')

    tree = ET.parse(cts_xml_file_name)
    root = tree.getroot()

    i = 1

    for test_packages in root.findall('TestPackage'):
        test_packages_name = test_packages.attrib.get('name')

        for test_cases in test_packages.iter("TestCase"):        
            test_cases_name = test_cases.attrib.get('name')

            for test_name in test_cases.iter("Test"):
                test_spec_name = test_name.attrib.get('name')
                test_spec_result = test_name.attrib.get('result')

                if (test_spec_result.find('fail') == 0):
                    fail_scene = test_name.getchildren()
                    fail_scene_message = fail_scene[0].attrib.get('message')

                    stack_trace = fail_scene[0].getchildren()
                    stack_trace_content = stack_trace[0].text

                    if (i % 2 == 0):
                        worksheet.write(i, 0, test_packages_name, style)
                        worksheet.write(i, 1, test_cases_name, style)
                        worksheet.write(i, 2, test_spec_name, style)
                        worksheet.write(i, 3, test_spec_result, style)
                        worksheet.write(i, 4, fail_scene_message, style)
                        worksheet.write(i, 5, stack_trace_content, style)
                    else:
                        worksheet.write(i, 0, test_packages_name, style2)
                        worksheet.write(i, 1, test_cases_name, style2)
                        worksheet.write(i, 2, test_spec_name, style2)
                        worksheet.write(i, 3, test_spec_result, style2)
                        worksheet.write(i, 4, fail_scene_message, style2)
                        worksheet.write(i, 5, stack_trace_content, style2)
                    i = i + 1
                    
    # save parsed results into excel file
    workbook.save(parser_result_excel_file_name)

    # return failure count
    return i-1

if __name__=="__main__":
    if 3 <= len(sys.argv) < 4: 
        print 'cts xml result parser : Initializing' 
        i = cts_result_parser(sys.argv[1], sys.argv[2])
        print 'cts xml result parser : ' + str(i) + ' failures of CTS are parsed.'
        print 'cts xml result parser : Finished' 
    else: 
        print '=' * 90
        print '= '
        print '=  Usage: python %s cts_xml_result_fn parser_result_excel_fn' % sys.argv[0] 
        print '= '
        print '=' * 90
