from selenium import webdriver
import requests
import re
import xlwt


def getPage(url):
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(url)
    return browser.page_source


def extract(list):
    compile1 = re.compile(r'<.+">')
    compile2 = re.compile(r'</.+>')
    for j in range(len(list)):
        list[j] = (re.sub(compile2, '', re.sub(compile1, '', list[j])))
    return list


def parserHTML(response, movieInfo):
    fraction = re.findall(r'<i class="fraction">\d?</i>', response)  # 评分小数位
    fraction = extract(fraction)
    integer = re.findall(r'<i class="integer">\d?.?</i>', response)  # 评分整数位
    integer = extract(integer)

    grade = []
    for j in range(len(fraction)):
        grade.append(integer[j] + fraction[j])

    releasetime = re.findall(r'<p class="releasetime">.+</p>', response)  # 上映时间
    releasetime = extract(releasetime)
    for j in range(len(releasetime)):
        releasetime[j] = releasetime[j].replace('上映时间：', '')

    ranking = re.findall(r'<i class="board-index board-index-\d+">\d+</i>', response)  # 排名
    ranking = extract(ranking)

    star = re.findall(r'<p class="star">\s*.+\s*</p>', response)  # 演员
    star = extract(star)
    for j in range(len(star)):
        star[j] = re.sub(r'(\s*)', '', star[j])
        star[j] = star[j].replace('主演：', '')

    for j in range(len(star)):
        movieInfo.append([eval(ranking[j]), eval(grade[j]), releasetime[j], star[j]])
    return movieInfo


def writeToExcel(movieInfo):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('猫眼top100')
    worksheet.write(0, 0, '排位')
    worksheet.write(0, 1, '评分')
    worksheet.write(0, 2, '上映时间')
    worksheet.write(0, 3, '演员')
    for i in range(len(movieInfo)):
        for j in range(len(movieInfo[i])):
            worksheet.write(i+1,j,movieInfo[i][j])
    workbook.save('猫眼top100.xls')


def main():
    movieInfo = []
    for i in range(10):
        url = 'https://maoyan.com/board/4?offset=' + str(i * 10)
        response = getPage(url)
        parserHTML(response, movieInfo)
    print(len(movieInfo))
    writeToExcel(movieInfo)


if __name__ == '__main__':
    main()
