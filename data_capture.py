import tools as tl



def make_list_of_all_pages():
    list_of_all_pages = []
    list_of_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                       'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    for element in list_of_letters:
        list_of_all_pages.append(('http://en.hispanosnba.com/players/nba-all/{}'.format(element), "players_{}.html".format(element)))        

    return list_of_all_pages


def save_all_pages():
    list_of_pages = make_list_of_all_pages()
    for (page, name) in list_of_pages:
        tl.save_page_to_file(page, name)


           


    
