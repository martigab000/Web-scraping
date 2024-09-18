import httpx
import os
import csv
import requests
from selectolax.parser import HTMLParser
import pandas as pd
import datetime
import hashlib

lst = [] your mom stinks
new_run = datetime.datetime.now().strftime("%Y-%m-%d")
new_folder = str(new_run)
# print(new_folder)

def main():
    ex_file = './files/Claim Knowledge Base - 5.26.23.xlsx'
    datas = pd.read_excel(ex_file)
    for i, data in datas.iterrows():
        url = data['URLs']
        selector = data['Selector']
        loc = data['Name']
        try:
            if type(loc) != float:   
                # print(loc, url, selector)
                new_file = f"{new_folder}/{str(loc)}"
                chk_dir(info=new_file)
                get_info(loc, url, selector)
        except BaseExceptionGroup():
            # chk_dir(info=new_run)
            print()
            return
        
def hash(text):
    h = hashlib.new("SHA256")
    text = "temp"
    h.update(text.encode())
    text_hash = h.hexdigest()
    #hash input
    if input != hash:
        create_txt()
        

def chk_dir(info):
    dir = f"./data/{info}"
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("directory created:", dir)
    else:
        print("directory already exists:", dir)
        
    
def create_txt(info, loc):
    text_file = f"./data/{new_folder}/{loc}/info.csv"
    with open(text_file, 'a', encoding='utf-8', newline="") as file:
        writer = csv.writer(file)
        writer.writerow([info])
        
def import_docs(file_name, q_link, loc):
    print(loc)
    #handles error caused by / in names of file
    
    if file_name.__contains__("/"):
        file_name = str(file_name).replace("/", "")
    if file_name.startswith('Chapter 24 - General'):
        file_name = "chapter 24 - General.pdf"
    output_dir = f'./data/{new_folder}/{loc}'
    if os.path.exists(output_dir):
        file_path = os.path.join(output_dir, file_name)
        print(file_path)
        
        #check if file exist in output directory
        if os.path.exists(file_path):
            print(f"{file_name} already exists in {output_dir}")
            return
        response = requests.get(q_link) #get website information 
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content) #write the file to the directory with the new file location and the contents from the website
                print(f"{file_name} downloaded and saved to {output_dir}")
        else:
            print(f"Error downloading {file_name}. Status code: {response.status_code}")
    else:
        print("error with parent dir")
        

def get_info(loc, url, selector):
    resp = httpx.get(
        url, 
        headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
        }
    )
    
    html = HTMLParser(resp.text)
    nodes = html.css(selector)
    if loc == "CMS":
        for node in nodes:
            link=node.css_first('a')
            file_name = link.text(strip=True)
            link = link.attributes['href']
            link = f"https://www.cms.gov{link}"
            file = f"{file_name}.pdf"
            # print(file_name, link)
            import_docs(file_name=file,q_link=link,loc=loc)

    elif str(url).endswith(".pdf"):
        file = f"{loc}.pdf"
        import_docs(file_name=file, q_link=url,loc=loc)
    elif str(url).endswith(".xlsx"):
        file = f"{loc}.xlsx"
        import_docs(file_name=file, q_link=url,loc=loc)
            
    elif loc == "ngs":
        for node in nodes:
            tbody = node.css_first('tbody')
            txts = tbody.css('div.container-fluid')
            for txt in txts:
                text = txt.text(strip=True)
                create_txt(info=text,loc=loc)
                
    elif loc == "x12":
        nodes = html.css_first(selector)
        nodes = nodes.css('tbody')
        for node in nodes:
            l_nodes = node.css('tr')
            for l_node in l_nodes:
                link = l_node.css_first('a')
                file_name = link.text(strip=True)
                link = link.attributes['href']
                link = f"https://x12.org{link}"
                x_data(url=link,loc=loc)
                
    elif loc == "uhc-gen":
        nodes = html.css_first('div.responsivegrid.leftnav-wrap-border.aem-GridColumn.aem-GridColumn--default--12')
        nodes = nodes.css('a')
        for node in nodes:
            l_node = node.css_first('a')
            if l_node.attributes.__contains__('href'):
                if str(l_node.attributes['href']).startswith("h"):
                    link = l_node.attributes['href']
                    if link not in lst:
                        lst.append(link)
                        if str(link).endswith(".pdf") == True:
                            file_name = l_node.text(strip=True)
                            file_name = f"{file_name}.pdf"
                            # print(f"full link pdf    {file_name}, {link}")
                            import_docs(file_name=file_name, q_link=link,loc=loc)
                            pass
                        else:
                            # print(f"full link else   {link}")
                            x_data(link,loc=loc)
                elif str(l_node.attributes['href']).startswith("/") == True:
                    link = l_node.attributes['href']
                    link = f"https://www.uhcprovider.com{link}"
                    if str(link).endswith(".pdf") == True:
                        file_name = l_node.text(strip=True)
                        file_name = f"{file_name}.pdf"
                        # print(f"half link pdf    {file_name}, {link}")
                        import_docs(file_name=file_name, q_link=link,loc=loc)
                        pass
                    else:
                        # print(f"half link else   {link}")
                        x_data(link,loc=loc)
            else:
                pass  
    elif loc == "uhc-info":
        
        domain = "https://www.uhc"
        info = html.css_first('div.regioncontainer.responsivegrid.aem-GridColumn--default--none.aem-GridColumn--default--9.aem-GridColumn.aem-GridColumn--offset--default--0')
        t_nodes = info.css('p')
        for t_node in t_nodes:
            text = t_node.css_first('p').text(strip=True)
            # print(text)
            create_txt(text,loc=loc)
        nodes = info.css('a')
        for node in nodes:
            l_node = node.css_first('a')
            if l_node.attributes.__contains__('href'):
                    if str(l_node.attributes['href']).startswith("h"):
                        if str(l_node.attributes['href']).startswith(domain):
                            link = l_node.attributes['href']
                            if link not in lst:
                                lst.append(link)
                                if str(link).endswith(".pdf") == True:
                                    file_name = l_node.text(strip=True)
                                    file_name = f"{file_name}.pdf"
                                    # print(f"full link pdf    {file_name}, {link}")
                                    import_docs(file_name=file_name, q_link=link,loc=loc)
                                    pass
                                else:
                                    # print(f"full link else   {link}")
                                    x_data(link,loc=loc)
                        else:
                            pass
                    elif str(l_node.attributes['href']).startswith("/") == True:
                        link = l_node.attributes['href']
                        link = f"https://www.uhc.com{link}"
                        if str(link).endswith(".pdf") == True:
                            file_name = l_node.text(strip=True)
                            file_name = f"{file_name}.pdf"
                            # print(f"half link pdf    {file_name}, {link}")
                            import_docs(file_name=file_name, q_link=link,loc=loc)
                            pass
                        else:
                            # print(f"half link else   {link}")
                            x_data(link,loc=loc)
            else:
                pass
        
            
    elif loc == "uhc":
        title_n = html.css_first('div.rte.component.container.padding.rteAnalytics')
        title = title_n.css_first('p').text(strip=True)
        # print(title)
        create_txt(title,loc=loc)
        nodes = html.css('div.columncontainer.aem-GridColumn--phone--12.aem-GridColumn.aem-GridColumn--default--12')
        for node in nodes:
            p_nodes = node.css('p')
            l_nodes = node.css('a')
            for p_node in p_nodes:
                text = p_node.css_first('p').text(strip=True)
                # print(text)
                create_txt(text,loc=loc)
            for l_node in l_nodes:
                if str(l_node.css_first('a').attributes['href']).endswith('.pdf'):
                    file_name = l_node.text(strip=True)
                    file_name = f"{file_name}.pdf"
                    link = l_node.css_first('a').attributes['href'].strip()
                    link = f"https://www.uhcprovider.com{link}"
                    # print(file_name, link)
                    import_docs(file_name=file_name, q_link=link,loc=loc)
                else:
                    pass
                
    elif loc == "caqh":
        l_node = html.css_first('div.region.region-content')
        file_name = l_node.css_first('a').text(strip=True)
        link = l_node.css_first('a').attributes['href']
        file = f"{file_name}.xlsx"
        import_docs(file_name=file, q_link=link,loc=loc)
        

def x_data(url, loc):
    resp = httpx.get(
        url, 
        headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
        }
    )
    html = HTMLParser(resp.content)
    if url == "https://x12.org/codes/property-casualty-code-lists":
        nodes = html.css_first('div#content-area')#content-area
        nodes = nodes.css('div.code_list_accordion__code-list-table')
        for node in nodes:
            t_nodes = node.css('td')
            for t_node in t_nodes:
                text = t_node.css_first('td').text(strip=True)        
                create_txt(info=text,loc=loc)
                # print(temp)
    elif url == "https://x12.org/codes/provider-taxonomy-codes" or str(url).startswith("https://chameleoncloud.io/"):
        pass
    elif url == "https://www.uhcprovider.com/en/resource-library/edi/edi-benefits.html" or url == "https://www.uhcprovider.com/en/resource-library/edi/edi-quick-tips-claims.html":
        nodes = html.css('div.accordionitem.panel-default.panel')
        for node in nodes:
            t_nodes = node.css('p')
            for t_node in t_nodes:
                text = t_node.css_first('p').text(strip=True)
                create_txt(text,loc=loc)
                # print(text)
    elif str(url).startswith("https://www.uhcprovider.com") or str(url).startswith("http://www.uhcprovider.com"):
        nodes = html.css('div.richtext.text.aem-GridColumn--phone--12.aem-GridColumn--default--9.aem-GridColumn')
        for node in nodes:
            t_nodes = node.css('p')
            for t_node in t_nodes:
                text1 = t_node.css_first('p').text(strip=True)
                create_txt(text1,loc=loc)
                # print(text1)
            b_nodes = node.css('li')
            for b_node in b_nodes:
                text2 = b_node.css_first('li').text(strip=True)
                create_txt(text2,loc=loc)
                # print(text2)
    # elif url == "https://view-awesome-table.com/-MZTdtM2V0ihM0-nUJKe/view":
    #     nodes = html.css('div.body-child.google-visualization-controls-theme-plus.at-layout-vertical')
    #     print(nodes)
    #     for node in nodes:
    #         text = node.css_first('div').child
        
    #         print(nodes)
            
    elif str(url).startswith("https://www.uhc"):
        nodes = html.css('div.responsivegrid.aem-GridColumn.aem-GridColumn--default--12')
        domain = "https://www.uhc"
        for node in nodes:
            t_nodes = node.css('p')
            l_nodes = node.css('a')
            for t_node in t_nodes:
                text = t_node.css_first('p').text(strip=True)
                # print(text)
                create_txt(text,loc=loc)
            for l_node in l_nodes:
                if l_node.attributes.__contains__('href') != False:
                    if str(l_node.attributes['href']).startswith("h") == True:
                        if str(l_node.attributes['href']).startswith(domain) == True:
                            link = l_node.attributes['href']
                            if link not in lst:
                                lst.append(link)
                                if str(link).endswith(".pdf") == True:
                                    file_name = l_node.text(strip=True)
                                    file_name = f"{file_name}.pdf"
                                    # print(f"full link pdf    {file_name}, {link}")
                                    import_docs(file_name=file_name, q_link=link,loc=loc)
                                    pass
                                elif str(link).endswith(".xlsx") == True:
                                    file_name = l_node.text(strip=True)
                                    file_name = f"{file_name}.xlsx"
                                    # print(f"full link pdf    {file_name}, {link}")
                                    import_docs(file_name=file_name, q_link=link,loc=loc)
                                    pass
                                else:
                                    # print(f"full link else   {link}")
                                    x_data(link,loc=loc)
                            else:
                                pass
                        else:
                            pass
                    elif str(l_node.attributes['href']).startswith("/") == True:
                        link = l_node.attributes['href']
                        link = f"https://www.uhc.com{link}"
                        if link not in lst:
                            lst.append(link)
                            if str(link).endswith(".pdf") == True:
                                file_name = l_node.text(strip=True)
                                file_name = f"{file_name}.pdf"
                                # print(f"half link pdf    {file_name}, {link}")
                                import_docs(file_name=file_name, q_link=link,loc=loc)
                                pass
                            elif str(link).endswith(".xlsx") == True:
                                file_name = l_node.text(strip=True)
                                file_name = f"{file_name}.xlsx"
                                # print(f"half link pdf    {file_name}, {link}")
                                import_docs(file_name=file_name, q_link=link,loc=loc)
                                pass
                            else:
                                # print(f"half link else   {link}")
                                x_data(link,loc=loc)
                        else:
                            pass
                    else:
                        pass    
                else:
                    pass
    else:
        nodes = html.css_first('div.code_list__code-list-table')
        nodes = nodes.css_first('tbody')
        nodes = nodes.css('td')
        for node in nodes:
            text = node.css_first('td').text(strip=True)
            create_txt(info=text,loc=loc)
    
# def create_parse(url):
#     try:
#         resp = httpx.get(
#             url, 
#             headers={
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
#             }
#         )
#     except httpx.ConnectError as e:
#         print(e)
#         pass
#     else:
#         html = HTMLParser(resp.content)
#         return html

# def scrape_text(url, selector, **selector1):
#     html = create_parse(url)
#     nodes = html.css('div.accordionitem.panel-default.panel')
#     for node in nodes:
#         if node.attributes.__contains__('p'):
#             t_nodes = node.css('p')
#             for t_node in t_nodes:
#                 text = t_node.css_first('p').text(strip=True)
#                 create_txt(text)
#         if node.attributes.__contains__(selector1):#'li'
#             b_nodes = t_node.css(selector1)
#             for b_node in b_nodes:
#                 text2 = b_node.css_first(selector1).text(strip=True)
#                 create_txt(text2)

# def scrape_url(url, selector, domain):
#     html = create_parse(url)
#     nodes = html.css_first(selector)#'div.responsivegrid.leftnav-wrap-border.aem-GridColumn.aem-GridColumn--default--12'
#     nodes = nodes.css('a')
#     for node in nodes:
#         l_node = node.css_first('a')
#         if l_node.attributes.__contains__('href'):
#             if str(l_node.attributes['href']).startswith("h"):
#                 if str(l_node.attributes['href']).startswith(domain):
#                     link = l_node.attributes['href']
#                     if link not in lst:
#                         lst.append(link)
#                         if str(link).endswith(".pdf"):
#                             file_name = l_node.text(strip=True)
#                             file_name = f"{file_name}.pdf"
#                             # print(f"full link pdf    {file_name}, {link}")
#                             import_docs(file_name=file_name, q_link=link)
#                             pass
#                         else:
#                             # print(f"full link else   {link}")
#                             x_data(link)
#             elif str(l_node.attributes['href']).startswith("/"):
#                 link = l_node.attributes['href']
#                 link = f"https://www.uhcprovider.com{link}"
#                 if str(link).endswith(".pdf") == True:
#                     file_name = l_node.text(strip=True)
#                     file_name = f"{file_name}.pdf"
#                     # print(f"half link pdf    {file_name}, {link}")
#                     import_docs(file_name=file_name, q_link=link)
#                     pass
#                 else:
#                     # print(f"half link else   {link}")
#                     x_data(link)
#         else:
#             pass  
    

# def scrape_all(url, selector, domain, ):
#     html = create_parse(url=url)
#     nodes = html.css(selector)#'div.responsivegrid.aem-GridColumn.aem-GridColumn--default--12'
#     # domain = "https://www.uhc"
#     for node in nodes:
#         t_nodes = node.css('p')
#         l_nodes = node.css('a')
#         for t_node in t_nodes:
#             text = t_node.css_first('p').text(strip=True)
#             # print(text)
#             create_txt(text)
#         for l_node in l_nodes:
#             if l_node.attributes.__contains__('href'):
#                 if str(l_node.attributes['href']).startswith("h"):
#                     if str(l_node.attributes['href']).startswith(domain):
#                         link = l_node.attributes['href']
#                         if link not in lst:
#                             lst.append(link)
#                             if str(link).endswith(".pdf"):
#                                 file_name = l_node.text(strip=True)
#                                 file_name = f"{file_name}.pdf"
#                                 # print(f"full link pdf    {file_name}, {link}")
#                                 import_docs(file_name=file_name, q_link=link)
#                                 pass
#                             elif str(link).endswith(".xlsx") == True:
#                                 file_name = l_node.text(strip=True)
#                                 file_name = f"{file_name}.xlsx"
#                                 # print(f"full link pdf    {file_name}, {link}")
#                                 import_docs(file_name=file_name, q_link=link)
#                                 pass
#                             else:
#                                 # print(f"full link else   {link}")
#                                 x_data(link)
#                         else:
#                             pass
#                     else:
#                         pass
#                 elif str(l_node.attributes['href']).startswith("/"):
#                     link = l_node.attributes['href']
#                     link = f"https://www.uhc.com{link}"
#                     if link not in lst:
#                         lst.append(link)
#                         if str(link).endswith(".pdf"):
#                             file_name = l_node.text(strip=True)
#                             file_name = f"{file_name}.pdf"
#                             # print(f"half link pdf    {file_name}, {link}")
#                             import_docs(file_name=file_name, q_link=link)
#                             pass
#                         elif str(link).endswith(".xlsx"):
#                             file_name = l_node.text(strip=True)
#                             file_name = f"{file_name}.xlsx"
#                             # print(f"half link pdf    {file_name}, {link}")
#                             import_docs(file_name=file_name, q_link=link)
#                             pass
#                         else:
#                             # print(f"half link else   {link}")
#                             x_data(link)
#                     else:
#                         pass
#                 else:
#                     pass    
#             else:
#                 pass     
    
if __name__ == "__main__":
    main()