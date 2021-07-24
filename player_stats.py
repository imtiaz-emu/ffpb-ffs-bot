def player(page_source, stats_type, stats):
  if stats_type == 'involvement':
    stats = involvement(page_source, stats)
  elif stats_type == 'expected':
    stats = expected(page_source, stats)
  elif stats_type == 'keeping':
    stats = keeping(page_source, stats)

  return stats


def involvement(page_source, stats):
  for indx, row_data in enumerate(page_source.find_elements_by_css_selector('td'), start=0):
    # 2nd column of the table contains team name
    if indx == 1:
      stats['team'] = row_data.text.strip()
    # 3rd column of the table contains player fpl price
    if indx == 2:
      stats['price'] = row_data.text.strip()
    if indx == 4:
      stats['min_played'] = row_data.text.strip()
    if indx == 5:
      stats['touches']['total'] = row_data.text.strip()
    if indx == 6:
      stats['touches']['opp_half'] = row_data.text.strip()
    if indx == 7:
      stats['touches']['final_3rd'] = row_data.text.strip()
    if indx == 8:
      stats['touches']['mins_per_tch'] = row_data.text.strip()
    if indx == 9:
      stats['passes']['total'] = row_data.text.strip()
    if indx == 10:
      stats['passes']['opp_half'] = row_data.text.strip()
    if indx == 11:
      stats['passes']['final_3rd'] = row_data.text.strip()
    if indx == 12:
      stats['passes']['mins_per_pass'] = row_data.text.strip()

  return stats


def expected(page_source, stats):
  for indx, row_data in enumerate(page_source.find_elements_by_css_selector('td')):
    if indx == 3:
      stats['expected']['assists'] = row_data.text.strip()
    if indx == 4:
      stats['expected']['xA'] = row_data.text.strip()
    if indx == 7:
      stats['expected']['goals'] = row_data.text.strip()
    if indx == 8:
      stats['expected']['xG'] = row_data.text.strip()

  return stats

def keeping(page_source, stats):
  for indx, row_data in enumerate(page_source.find_elements_by_css_selector('td')):
    if indx == 6:
      stats['keeping']['saves'] = row_data.text.strip()
    if indx == 7:
      stats['keeping']['goals_concede'] = row_data.text.strip()
    if indx == 10:
      stats['keeping']['pen_saves'] = row_data.text.strip()

  return stats


def build_player_stats(page_source):
  players = []

  for player_involvement in page_source.find_elements_by_css_selector('#player-tabs-2 tbody tr'):
    for indx, row_data in enumerate(player_involvement.find_elements_by_css_selector('td')):
      if indx == 0:
        player_name = row_data.find_element_by_css_selector('.profile-title').text.split('\n')[0].strip()
        stats = {}
        stats[player_name] = {}
        stats[player_name]['touches'], stats[player_name]['passes'], stats[player_name]['expected'], stats[player_name]['keeping'] = {}, {}, {}, {}
        players.append(stats)

  return players


def filter_player_by_name(players, player_name):
  filter_players = list(filter(lambda player: list(player.keys())[0] == player_name, players))

  if len(filter_players) > 0:
    return filter_players[0]
  else:
    return None