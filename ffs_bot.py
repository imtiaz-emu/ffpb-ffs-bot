'''
Python: > 3.7
Author: Md Imtiaz Hossain Emu
About: Fantasy Football Scout - match stats scrapper
'''

from selenium import webdriver
from time import sleep
from pathlib import Path
import os, json, sys
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from constants import constants
from player_stats import player, build_player_stats

class FFS_BOT():

  def __init__(self, match_id):
    # settings for chrome driver
    load_dotenv(dotenv_path='{base_path}/.env'.format(base_path=str(Path(__file__).resolve().parent)))
    self.browser = webdriver.Chrome(os.getenv('WEBDRIVER_PATH'), options=self.chrome_driver_options())
    # add 'implicitly_wait' just to give N seconds time to to load full page with all plugins and assets
    # self.browser.implicitly_wait(3)
    self.match_id = match_id.strip()
    self.player_stats = []

  def login_to_ffs(self):
    ffs_username = os.getenv('FFS_USERNAME')
    ffs_password = os.getenv('FFS_PASSWORD')
    ffs_login_url = 'https://members.fantasyfootballscout.co.uk/'

    self.browser.get(ffs_login_url)

    try:
      element = WebDriverWait(self.browser, 20).until(
        EC.presence_of_element_located((By.ID, "username"))
      )

      if "Please wait a few minutes" in self.browser.page_source:
        self.save_page_as_file({}, 'match_stats.json')
        self.browser.quit()

      username_input = self.browser.find_element_by_xpath("//input[@name='username']")
      password_input = self.browser.find_element_by_xpath("//input[@name='password']")

      username_input.send_keys(ffs_username)
      password_input.send_keys(ffs_password)
      password_input.send_keys(Keys.ENTER)
    except Exception as e:
      self.browser.refresh()


  def collect_page_data(self):
    match_stats_url = 'https://members.fantasyfootballscout.co.uk/matches/{m_id}/'.format(m_id=self.match_id)
    # The following is a sample match stats page collected and saved as html locally to extract data without hitting the ffs server
    # match_stats_url = 'file:///Users/imtiaz/Etectra/work/ffs-ffpb/match_stats.html'
    self.browser.get(match_stats_url)
    self.player_stats = build_player_stats(self.browser)

    try:
      self.extract_data_from_page()
      self.player_stats = self.format_stats()
      result = json.dumps(self.player_stats)
      self.save_page_as_file(result, 'match_stats.json')

      self.browser.quit()
    except Exception as e:
      print(e)
      self.browser.quit()


  def extract_data_from_page(self):
    for player_stat in self.player_stats:
      player_name = list(player_stat.keys())[0]

      for tab_id, tab_type in constants.items():
        for player_involvement in self.browser.find_elements_by_css_selector('{tab_id} tbody tr'.format(tab_id=tab_id)):
          row_player_name = player_involvement.find_element_by_css_selector('td .profile-title').text.split('\n')[0].strip()
          if row_player_name == player_name:
            player_stat[player_name] = player(player_involvement, tab_type, player_stat[player_name])
            break


  def format_stats(self):
    formatted_stats = []

    for player_stat in self.player_stats:
      player_name = list(player_stat.keys())[0]
      player_stats_data = list(player_stat.values())[0]
      formatted_stats.append({'Player': player_name, 'Stats': player_stats_data})

    return formatted_stats

  def chrome_driver_options(self):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--always-authorize-plugins')
    return chrome_options

  def save_page_as_file(self, data, file_name = 'match_stats.html'):
    file_path = str(Path(__file__).resolve().parent) + '/' + file_name

    with open(file_path, "w") as f:
      f.write(data)


bot = FFS_BOT(sys.argv[1])
bot.login_to_ffs()
sleep(3)
bot.collect_page_data()
