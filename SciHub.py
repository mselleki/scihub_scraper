from selenium import webdriver
import time

xpath_text = '//*[@id="id_term"]'
xpath_button = '//*[@id="search-form"]/div[1]/div[1]/div/button'

pmid_xpath = '//*[@id="search-results"]/section/div[1]/div/article[1]/div[2]/div[1]/div[1]/span[5]/span'

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": "/home/icrin_3/Downloads/Articles_dl",  # Change default directory for downloads
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
})

options.add_argument('headless')


def pmid_scraper(key_words):
    driver = webdriver.Chrome('/home/icrin_3/Téléchargements/chromedriver', options=options)
    driver.get('https://pubmed.ncbi.nlm.nih.gov/')
    driver.find_element_by_xpath('//*[@id="id_term"]').send_keys(key_words)  # request
    driver.find_element_by_xpath(xpath_button).click()
    pmid = driver.find_element_by_class_name('docsum-pmid').text
    driver.close()
    return pmid


def pub_med_results(key_words, nb_results):
    dic_results = {}
    driver = webdriver.Chrome('/home/icrin_3/Téléchargements/chromedriver', options=options)
    driver.get('https://pubmed.ncbi.nlm.nih.gov/')
    driver.find_element_by_xpath('//*[@id="id_term"]').send_keys(key_words)  # request
    driver.find_element_by_xpath(xpath_button).click()
    max_result = int(driver.find_element_by_xpath('//*[@id="search-results"]/div[2]/div[1]/span').text)
    if nb_results > int(max_result):
        nb_results = int(max_result)
    for i in range(nb_results):
        result = driver.find_element_by_xpath(f'//*[@id="search-results"]/section/div[1]/div/article[{i + 1}]/div['
                                              f'2]/div[1]/a')
        pmid = driver.find_element_by_xpath(f'//*[@id="search-results"]/section/div[1]/div/article[{i + 1}]/div[2]/div['
                                            f'1]/div[1]/span[5]/span')
        dic_results[i + 1] = int(pmid.text)
        print(str(i + 1) + ' - ' + result.text + '\n')
    driver.close()
    return dic_results, max_result


def read_abstract(pmid):
    driver = webdriver.Chrome('/home/icrin_3/Téléchargements/chromedriver', options=options)
    driver.get('https://pubmed.ncbi.nlm.nih.gov/')
    driver.find_element_by_xpath('//*[@id="id_term"]').send_keys(str(pmid))  # request
    driver.find_element_by_xpath(xpath_button).click()
    abstract = driver.find_element_by_xpath('//*[@id="enc-abstract"]')
    print(abstract.text)
    driver.close()
    return abstract


# Second part : download of the article


# noinspection PyBroadException
def article_scraper(pmid):
    driver = webdriver.Chrome('/home/icrin_3/Téléchargements/chromedriver', options=options)
    driver.get('https://sci-hub.se')
    driver.find_element_by_xpath('//*[@id="input"]/form/input[2]').send_keys(pmid)
    driver.find_elements_by_id("open")[0].click()
    link_dl = str(driver.find_elements_by_xpath('//*[@id="buttons"]/button')[0].get_attribute('onclick'))
    if link_dl[-1] == '/' or link_dl[-1] == "'":
        link_dl = link_dl[:-1]

    if link_dl[link_dl.find("'") + 1] == '/':
        link_dl = link_dl.replace('//', '')  # often double dash

    if link_dl.find('https') == -1 and link_dl.find('http') == -1:
        link_dl = 'https://' + link_dl[link_dl.find("'") + 1:]
    else:
        link_dl = link_dl[link_dl.find("'") + 1:]

    print('Graal founded !' + link_dl)
    try:
        driver.get(link_dl)
        print("Download was a success. Don't tell anyone about this program please.")
    except:
        print("There was an error. Please contact chief administrator officer. Or try again.")
    driver.close()


research = input("Key words : ")
results = int(input('Would his Majesty inform us how many results he desires ? '))
PMID = pmid_scraper(research)
Dico_Res, max_r = pub_med_results(research, results)
abs_art_nb = int(input('Would his Majesty like to read an abstract of any of these articles ? Yes [number of article] '
                       'Exit [9]\n'))
while abs_art_nb > max_r or type(abs_art_nb) is not int or abs_art_nb < 0:
    abs_art_nb = int(
        input('Would his Majesty like to read an abstract of any of these articles ? Yes [number of article] '
              'Exit [9]\n'))

if abs_art_nb == 0:
    exit()
else:
    read_abstract(Dico_Res[abs_art_nb])
    dl = int(input("Would his Majesty like to download this article ? Yes [1], Back to Menu [0], Exit [9] \n"))
    if dl == 1:
        article_scraper(Dico_Res[abs_art_nb])
    if dl == 0:
        pub_med_results(research, results)
        # code the menu

    if dl == 9:
        exit()


# article_scraper(PMID)
