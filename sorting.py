import tools as tl
import re



regex_player = re.compile(
    r'<tr.*?>'
    r'<th scope="row" class="tdl fn.*?>'
    r'<a href="/players/(?P<player_link>.*?)' #PLAYER'S LINK
    r'" title=".*?">'
    r'(?P<player_name>.*?)</a>' #NAME
    r'<td>(?P<position>.*?)' #POSITION
    r'<td>(?P<height>.*?)' #HEIGHT
    r'<td>(?P<from>.*?)' #FROM
    r'<td>(?P<to>.*?)' #TO
    r'<td class="tdc">(?P<seasons>\d+)' #SEASONS
    ,
    flags=re.DOTALL
    )


def make_html_list():
    '''Make list with all html files'''
    html_list = []
    list_of_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                       'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    for word in list_of_letters:
            html_list.append("players_{}.html".format(word))
    return html_list

def prepare_data(data):
    '''Edit the information in the dictionary'''
    data = data.groupdict()
    data['height'] = float(data['height'][:4])
    data['seasons'] = int(data['seasons'])
    return data
            
data_list = []
def prepare():
    '''Merge the data with a loop and save into a list'''
    html_list = make_html_list()
    for element in html_list:
        with open(element,encoding='utf8') as f:
            content_of_page = f.read()
            for match in regex_player.finditer(content_of_page):
                data_list.append(prepare_data(match)) #slovar - z zanko shranim v seznam
    


prepare()

tl.make_table(data_list, ['player_name', 'player_link', 'position', 'height', 'from', 'to', 'seasons'], 'players.csv')
                        


#get more data -> player link -> extra data ... skupi v en slovar         
        

    
