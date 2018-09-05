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

regex_player_more = re.compile(
    r'<div class="jugdatd"><ul class=" block">.*?'
    r'<li><strong>Full name:</strong>.*?</li>.*?'
    r'<li><strong>Nationality:</strong> <span itemprop="nationality">(?P<nationality>.*?)</span></li>.*?' #NAT
    r'<li><strong>College:</strong>\s(?P<college>.*?)\s.*?' #COLLEGE
    r'<li><strong>Draft:</strong> <a href=.*?>(?P<pick>.*?)</a>.*?' #DRAFT/PICK
    r'<td class="tdn">(?P<points_per_game>.*?)<t.*?' #PTS
    r'd>(?P<rebounds_per_game>.*?)<t.*?' #RB
    r'd>(?P<assists_per_game>.*?)<t.*?' #AS
    r'd>(?P<field_goals>.*?)<t.*?' #FG%
    r'd>(?P<three_points>.*?)<t.*?' #3P%
    r'd>(?P<free_throws>.*?)</table>.*?' #FT%
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
    '''Merges the data with a loop and save into a list'''
    html_list = make_html_list()
    for element in html_list:
        with open(element,encoding='utf8') as f:
            content_of_page = f.read()
            for match in regex_player.finditer(content_of_page):
                data_list.append(prepare_data(match)) #slovar - z zanko shranim v seznam
    return data_list
    


#EXTRA_DATA

data_list = prepare()

def make_list_of_extra_pages(data_list):
    list_of_extra = []
    for player in data_list:
        filename = str(player['player_link'])+".html"
        list_of_extra.append(('http://en.hispanosnba.com/amp/players/{}'.format(player['player_link']), filename))
    return list_of_extra

def save_extra_html(data_list):
    list_of_extra = make_list_of_extra_pages(data_list)
    for (player, name) in list_of_extra:
        tl.save_page_to_file(player, name)
    return
    
           
def extend_player_data(data_list):
    for player in data_list:
        filename = str(player['player_link'])+".html"
        with open(filename) as f:
            text = f.read()
            new_data = regex_player_more.find(text).groupdict()
            player.update(new_data)
    return


extend_player_data(data_list)

##def prepare2(data_list):
##    '''Extends prevoius data'''
##    html_list2 = save_extra_html(data_list)
##    for element in html_list2:
##        with open(element, encoding='utf8') as g:
##            content_of_page2 = g.read()
##            for match in regex_player_more.finditer(content_of_page2):
##                data_list.update(match)
##    return data_list
##
##        
##prepare2(data_list)

tl.make_table(data_list, ['player_name', 'player_link', 'position', 'height', 'from', 'to', 'seasons', 'nationality', 'college', 'draft', 'points_per_game', 'rebounds_per_game', 'assists_per_game',
                            'field_goals', 'three_points', 'free_throws'], 'players.csv')
        


    
#get more data -> player link -> extra data ... skupi v en slovar         
##        
##with open("test2.html") as f:
##    text = f.read()
##    print([x.groupdict() for x in regex_player_more.finditer(text)])
##    
    
