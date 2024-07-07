#
# data = {
#     'pagingPrevLink': {
#         'text': '<<',
#         'class': 'disabled'
#     },
#     'pagingNextLink': {
#         'text': '>>',
#         'class': 'disabled'
#     },
#     'pagingLinkPage1': {
#         'text': '1',
#         'class': 'current'
#     },
#     'pagingLinkPage2': {
#         'text': '2',
#         'class': ''
#     },
#     'pagingLinkPage3': {
#         'text': '3',
#         'class': ''
#     }
# }

def get_current_page(data: dict):
    """
    Метод для получения текущей страницы
    :param data: dict
    :return: int
    """
    for key, value in data.items():
        if value['class'] == 'current':
            return int(value['text'])

def get_max_page(data: dict):
    """
    Метод для получения максимальной страницы
    :param data: dict
    :return: int
    """
    max_page = 0
    for key, value in data.items():
        if value['text'].isdigit():
            if int(value['text']) > max_page:
                max_page = int(value['text'])
    return max_page
            
