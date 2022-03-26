#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@editors: Hadi El Karhani, Yorgo Bou Samra, Riad Jamal
"""

import pandas as pd #pip install pandas
import csv
import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup #pip install BeautifulSoup
import socket
import requests
from googlesearch import search #pip install googlesearch-python
import whois #pip install whois && pip install python-whois
from datetime import date, datetime
import time
from dateutil.parser import parse as date_parse

class FExtract:
    def __init__(self, index, data):
        self.index = index
        self.data = data

    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    def generate_data_set(self, url):

        data_set = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None, 11: None, 12: None, 13: None, 14: None, 15: None, 16: None, \
        17: None, 18: None, 19: None, 20: None, 21: None, 22: None, 23: None, 24: None, 25: None, 26: None, 27: None, 28: None, 29: None, 30: None}

        if not re.match(r"^https?", url):
            url = "http://" + url

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
            response = ""
            soup = -999

        domain = re.findall(r"://([^/]+)/?", url)[0]
        if re.match(r"^www.", domain):
            domain = domain.replace("www.", "")

        """ Changed here """
        try:
            whois_response = whois.whois(domain)

        except whois.parser.PywhoisError:
            self.data.drop([self.index], inplace = True) # Drop the row if domain doesn't exist and return None
            return None

        start = time.time()

        rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
            "name": domain
        })

        try:
            global_rank = int(re.findall(
                r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
        except:
            global_rank = -1

        # 1.having_IP_Address
        start = time.time()
        try:
            ipaddress.ip_address(url)
            data_set[1]=(-1)
        except:
            data_set[1]=(1)
        stop = time.time()
        duration = stop - start

        # 2.URL_Length
        start = time.time()
        if len(url) < 54:
            data_set[2]=(1)
        elif len(url) >= 54 and len(url) <= 75:
            data_set[2]=(0)
        else:
            data_set[2]=(-1)
        stop = time.time()
        duration = stop - start

        # 3.Shortining_Service
        start = time.time()
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                          'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                          'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                          'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                          'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                          'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                          'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url)
        if match:
            data_set[3]=(-1)
        else:
            data_set[3]=(1)
        stop = time.time()
        duration = stop - start

        # 4.having_At_Symbol
        start = time.time()
        if re.findall("@", url):
            data_set[4]=(-1)
        else:
            data_set[4]=(1)
        stop = time.time()
        duration = stop - start

        # 5.double_slash_redirecting
        start = time.time()
        list = [x.start(0) for x in re.finditer('//', url)]
        if list[len(list)-1] > 6:
            data_set[5]=(-1)
        else:
            data_set[5]=(1)
        stop = time.time()
        duration = stop - start

        # 6.Prefix_Suffix
        start = time.time()
        if re.findall(r"https?://[^\-]+-[^\-]+/", url):
            data_set[6]=(-1)
        else:
            data_set[6]=(1)
        stop = time.time()
        duration = stop - start

        # 7.having_Sub_Domain
        start = time.time()
        if len(re.findall("\.", url)) == 1:
            data_set[7]=(1)
        elif len(re.findall("\.", url)) == 2:
            data_set[7]=(0)
        else:
            data_set[7]=(-1)
        stop = time.time()
        duration = stop - start

        # 8.SSLfinal_State
        start = time.time()
        try:
            if response.text:
                data_set[8]=(1)
        except:
            data_set[8]=(-1)
        stop = time.time()
        duration = stop - start

        # 9.Domain_registeration_length
        start = time.time()
        expiration_date = whois_response.expiration_date
        registration_length = 0
        try:
            expiration_date = min(expiration_date)
            today = time.strftime('%Y-%m-%d')
            today = datetime.strptime(today, '%Y-%m-%d')
            registration_length = abs((expiration_date - today).days)

            if registration_length / 365 <= 1:
                data_set[9]=(-1)
            else:
                data_set[9]=(1)
        except:
            data_set[9]=(-1)
        stop = time.time()
        duration = stop - start

        # 10.Favicon
        start = time.time()
        if soup == -999 or str(soup) == "Too many requests":
            data_set[10]=(-1)

        else:
            try:
                for head in soup.find_all('head'):

                    if head.link == None: #CHANGE HERE
                        data_set[10]=(-1)
                        raise StopIteration

                    else:
                        for head.link in soup.find_all('link', href=True):
                            dots = [x.start(0)
                                    for x in re.finditer('\.', head.link['href'])]
                            if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                                data_set[10]=(1)
                                raise StopIteration
                            else:
                                data_set[10]=(-1)
                                raise StopIteration
            except StopIteration:
                pass
        stop = time.time()
        duration = stop - start

        # 11. port
        start = time.time()
        try:
            port = domain.split(":")[1]
            if port:
                data_set[11]=(-1)
            else:
                data_set[11]=(1)
        except:
            data_set[11]=(1)
        stop = time.time()
        duration = stop - start

        # 12. HTTPS_token
        start = time.time()
        if re.findall(r"^https://", url):
            data_set[12]=(1)
        else:
            data_set[12]=(-1)
        stop = time.time()
        duration = stop - start

        # 13. Request_URL
        start = time.time()
        i = 0
        success = 0
        if soup == -999:
            data_set[13]=(-1)
        else:
            for img in soup.find_all('img', src=True):
                dots = [x.start(0) for x in re.finditer('\.', img['src'])]
                if url in img['src'] or domain in img['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            for audio in soup.find_all('audio', src=True):
                dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
                if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            for embed in soup.find_all('embed', src=True):
                dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
                if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            for iframe in soup.find_all('iframe', src=True):
                dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
                if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            try:
                percentage = success/float(i) * 100
                if percentage < 22.0:
                    data_set[13]=(1)
                elif((percentage >= 22.0) and (percentage < 61.0)):
                    data_set[13]=(0)
                else:
                    data_set[13]=(-1)
            except:
                data_set[13]=(1)
        stop = time.time()
        duration = stop - start

        # 14. URL_of_Anchor
        start = time.time()
        percentage = 0
        i = 0
        unsafe = 0
        if soup == -999:
            data_set[14]=(-1)

        else:
            try:
                for a in soup.find_all('a', href=True):
                    # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and :: might not be
                        # there in the actual a['href']
                    if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                        unsafe = unsafe + 1
                    i = i + 1

                try:
                    percentage = unsafe / float(i) * 100
                except:
                    data_set[14]=(1)
                    raise StopIteration

                if percentage < 31.0:
                    data_set[14]=(1)
                    raise StopIteration

                elif ((percentage >= 31.0) and (percentage < 67.0)):
                    data_set[14]=(0)
                    raise StopIteration

                else:
                    data_set[14]=(-1)
                    raise StopIteration

            except StopIteration:
                pass
        stop = time.time()
        duration = stop - start

        # 15. Links_in_tags
        start = time.time()
        i = 0
        success = 0
        if soup == -999:
            data_set[15]=(-1)
            data_set[16]=(0)
        else:
            try:
                for link in soup.find_all('link', href=True):
                    dots = [x.start(0) for x in re.finditer('\.', link['href'])]
                    if url in link['href'] or domain in link['href'] or len(dots) == 1:
                        success = success + 1
                    i = i+1

                for script in soup.find_all('script', src=True):
                    dots = [x.start(0) for x in re.finditer('\.', script['src'])]
                    if url in script['src'] or domain in script['src'] or len(dots) == 1:
                        success = success + 1
                    i = i+1
                try:
                    percentage = success / float(i) * 100
                except:
                    data_set[15]=(1)
                    raise StopIteration

                if percentage < 17.0:
                    data_set[15]=(1)
                    raise StopIteration

                elif((percentage >= 17.0) and (percentage < 81.0)):
                    data_set[15]=(0)
                    raise StopIteration

                else:
                    data_set[15]=(-1)
                    raise StopIteration

            except StopIteration:
                pass
            stop = time.time()
            duration = stop - start

            # 16. SFH
            start = time.time()
            if len(soup.find_all('form', action=True))==0:
                data_set[16]=(1)
            else :
                for form in soup.find_all('form', action=True):
                    if form['action'] == "" or form['action'] == "about:blank":
                        data_set[16]=(-1)
                        break
                    elif url not in form['action'] and domain not in form['action']:
                        data_set[16]=(0)
                        break
                    else:
                        data_set[16]=(1)
                        break
            stop = time.time()
            duration = stop - start

        # 17. Submitting_to_email
        start = time.time()
        if response == "":
            data_set[17]=(-1)
        else:
            if re.findall(r"[mail\(\)|mailto:?]", response.text):
                data_set[17]=(-1)
            else:
                data_set[17]=(1)
        stop = time.time()
        duration = stop - start

        # 18. Abnormal_URL
        start = time.time()
        if response == "":
            data_set[18]=(-1)
        else:
            if response.text == whois_response:
                data_set[18]=(1)
            else:
                data_set[18]=(-1)
        stop = time.time()
        duration = stop - start

        # 19. Redirect
        start = time.time()
        if response == "":
            data_set[19]=(-1)
        else:
            if len(response.history) <= 1:
                data_set[19]=(-1)
            elif len(response.history) <= 4:
                data_set[19]=(0)
            else:
                data_set[19]=(1)
        stop = time.time()
        duration = stop - start

        # 20. on_mouseover
        start = time.time()
        if response == "":
            data_set[20]=(-1)
        else:
            if re.findall("<script>.+onmouseover.+</script>", response.text):
                data_set[20]=(1)
            else:
                data_set[20]=(-1)
        stop = time.time()
        duration = stop - start

        # 21. RightClick
        start = time.time()
        if response == "":
            data_set[21]=(-1)
        else:
            if re.findall(r"event.button ?== ?2", response.text):
                data_set[21]=(1)
            else:
                data_set[21]=(-1)
        stop = time.time()
        duration = stop - start

        # 22. popUpWidnow
        start = time.time()
        if response == "":
            data_set[22]=(-1)
        else:
            if re.findall(r"alert\(", response.text):
                data_set[22]=(1)
            else:
                data_set[22]=(-1)
        stop = time.time()
        duration = stop - start

        # 23. Iframe
        start = time.time()
        if response == "":
            data_set[23]=(-1)
        else:
            if re.findall(r"[<iframe>|<frameBorder>]", response.text):
                data_set[23]=(1)
            else:
                data_set[23]=(-1)
        stop = time.time()
        duration = stop - start

        # 24. age_of_domain
        start = time.time()
        if response == "":
            data_set[24]=(-1)
        else:
            try:
                registration_date = re.findall(
                        r'Registration Date:</div><div class="df-value">([^<]+)</div>', whois_response.text)[0]
                if diff_month(date.today(), date_parse(registration_date)) >= 6:
                    data_set[24]=(-1)
                else:
                    data_set[24]=(1)
            except:
                data_set[24]=(1)
        stop = time.time()
        duration = stop - start

        # 25. DNSRecord
        start = time.time()
        dns = 1
        try:
            d = whois.whois(domain)
        except:
            dns = -1
        if dns == -1:
            data_set[25]=(-1)
        else:
            if registration_length / 365 <= 1:
                data_set[25]=(-1)
            else:
                data_set[25]=(1)
        stop = time.time()
        duration = stop - start

        # 26. web_traffic
        start = time.time()
        try:
            rank = BeautifulSoup(urllib.request.urlopen(
                "http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
            rank = int(rank)
            if (rank < 100000):
                data_set[26]=(1)
            else:
                data_set[26]=(0)
        except :
            data_set[26]=(-1)
        stop = time.time()
        duration = stop - start

        # 27. Page_Rank
        start = time.time()
        try:
            if global_rank > 0 and global_rank < 100000:
                data_set[27]=(-1)
            else:
                data_set[27]=(1)
        except:
            data_set[27]=(1)
        stop = time.time()
        duration = stop - start

        # 28. Google_Index
        start = time.time()
        site = search(url, 5)
        if site:
            data_set[28]=(1)
        else:
            data_set[28]=(-1)
        stop = time.time()
        duration = stop - start

        # 29. Links_pointing_to_page
        start = time.time()
        if response == "":
            data_set[29]=(-1)
        else:
            number_of_links = len(re.findall(r"<a href=", response.text))
            if number_of_links == 0:
                data_set[29]=(1)
            elif number_of_links <= 2:
                data_set[29]=(0)
            else:
                data_set[29]=(-1)
        stop = time.time()
        duration = stop - start

        # 30. Statistical_report
        start = time.time()
        url_match = re.search(
            'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', url)
        try:
            ip_address = socket.gethostbyname(domain)
            ip_match = re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                                 '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                                 '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                                 '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                                 '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                                 '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42', ip_address)
            if url_match:
                data_set[30]=(-1)
            elif ip_match:
                data_set[30]=(-1)
            else:
                data_set[30]=(1)
        except:
            data_set[30]=(1)
            print('Connection problem. Please check your internet connection')
        stop = time.time()
        duration = stop - start

        return data_set
