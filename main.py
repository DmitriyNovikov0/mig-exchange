import requests
from bs4 import BeautifulSoup

URL = 'https://mig.kz/'
START_YEAR = 2023
START_MONTH = 1
START_DAY = 1
END_YEAR = 2023
END_MONTH = 12
END_DAY = 31


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def get_county_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = soup.find('ul', class_='pagination')
    if pagination is None:
        return 1
    else:
        count_pages = pagination.findAll('li')
        return len(count_pages)

def get_table(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table')
    if table is None:
        return 'Ошибка!!! парсинг таблицы с курсами не удался'
    else:
        return str(table)

def get_tbody(html):
    soup = BeautifulSoup(html, 'lxml')
    tb_body = soup.find('tbody')
    if tb_body is None:
        return 'Ошибка парсинга тела таблицы с курсами'
    else:
        return str(tb_body)

def get_thead(html):
    soup = BeautifulSoup(html, 'lxml')
    tb_head = soup.find('thead')
    if tb_head is None:
        return 'Ошибка парсинга шапки таблицы с курсами'
    else:
        return str(tb_head)


def main():
    table_text = '' + '\n'
    session = requests.Session()
    req = session.get(URL)

    my_data = {
        'page': '1',
        'from[day]': START_DAY,
        'from[month]': START_MONTH,
        'from[year]': START_YEAR,
        'to[day]': END_DAY,
        'to[month]': END_MONTH,
        'to[year]': END_YEAR,
        }
    req = session.post(URL + 'archive/search', my_data).text

    county_pages = get_county_pages(req)
    if county_pages > 1:
        table_text = '<table class="table table-hover">'
        table_text += get_thead(req) + '\n'
        for page_nmb in range(county_pages):
            print(f'страница: {page_nmb}')
            my_data['page'] = page_nmb
            req = session.post(URL + 'archive/search', my_data).text
            table_text += get_tbody(req)
        table_text += '</table>'
    else:
        table_text += get_table(req)

    # return
    if table_text is None:
        return
    else:
        file = open("table.html", "w")
        file.write(table_text)
        file.close()


if __name__ == '__main__':
    main()
