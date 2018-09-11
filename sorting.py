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
    r'd>(?P<free_throws>.*?)<.*?' #FT%
    ,
    flags=re.DOTALL
    )


def make_html_list():
    '''Makes list with all html files'''
    html_list = []
    list_of_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                       'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    for word in list_of_letters:
            html_list.append("players_{}.html".format(word))
    return html_list

def prepare_data(data):
    '''Edits the information in the dictionary'''
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
                data_list.append(prepare_data(match)) 
    return data_list
    


#EXTRA_DATA

data_list = prepare()

def make_list_of_extra_pages(data_list):
    '''Makes list with all extra html files'''
    list_of_extra = []
    for player in data_list:
        filename = str(player['player_link'])+".html"
        list_of_extra.append(('http://en.hispanosnba.com/amp/players/{}'.format(player['player_link']), filename))
    return list_of_extra

def make_list_of_extra_html(data_list):
    '''Makes list with extra html files'''
    list_of_extra_html = []
    for player in data_list:
        filename = str(player['player_link'])+".html"
        list_of_extra_html.append(filename)
    return list_of_extra_html
    

def save_extra_html(data_list):
    '''Saves extra html files'''
    list_of_extra = make_list_of_extra_pages(data_list)
    for (player, name) in list_of_extra:
        tl.save_page_to_file(player, name)
    return
    
def prepare_extra_data(data_list):
    '''Edits the information in the dictionary'''
    data_list['pick'] = int(data_list['pick'][13:])
    data_list['points_per_game'] = 0.0 if data_list['points_per_game'] == '--' else float(data_list['points_per_game'])
    data_list['rebounds_per_game'] = 0.0 if data_list['rebounds_per_game'] == '--' else float(data_list['rebounds_per_game'])
    data_list['assists_per_game'] = 0.0 if data_list['assists_per_game'] == '--' else float(data_list['assists_per_game'])
    data_list['field_goals'] = 0.0 if data_list['field_goals'] == '--' else float(data_list['field_goals'])
    data_list['three_points'] = 0.0 if data_list['three_points'] == '--' else float(data_list['three_points'])
    data_list['free_throws'] = 0.0 if data_list['free_throws'] == '--' else float(data_list['free_throws'])
    return data_list

def extend_player_data(data_list):
    '''Updates the previous data with extra'''
    for player in data_list:
        filename = str(player['player_link'])+".html"
        with open(filename) as f:
            text = f.read()
            print(player['player_link'])
            if [x.groupdict() for x in regex_player_more.finditer(text)] == []:
                pass
            else:
                new_data = [x.groupdict() for x in regex_player_more.finditer(text)][0]
            
##            player.update(prepare_extra_data(new_data))
                player.update(new_data)
                prepare_extra_data(player)
    return


##extend_player_data(data_list)



##tl.make_table(data_list, ['player_name', 'player_link', 'position', 'height', 'from', 'to', 'seasons', 'nationality', 'college', 'pick', 'points_per_game',
##                        'rebounds_per_game', 'assists_per_game', 'field_goals', 'three_points', 'free_throws'], 'players.csv')
##        
with open("goran-dragic.html") as f:
    text = f.read()
    print([x.groupdict() for x in regex_player_more.finditer(text)])

