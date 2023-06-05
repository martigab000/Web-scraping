import httpx
import os
import csv
import requests
from selectolax.parser import HTMLParser

lst = []
    
def create_txt(info):
    text_file = "./data/info.csv"
    with open(text_file, 'a', encoding='utf-8', newline="") as file:
        writer = csv.writer(file)
        writer.writerow([info])
        

def get_info(loc, url, selector):
    resp = httpx.get(
        url, 
        headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
        }
    )
    
    html = HTMLParser(resp.text)
    info = html.css(selector)
    if loc == "CMS":
        for item in info:
            link=item.css_first('a')
            file_name = link.text(strip=True)
            file_name = file_name.replace("/", "-")
            link = link.attributes['href']
            link = f"https://www.cms.gov{link}"
            loc = f"{file_name}.pdf"
            # print(file_name, link)
            import_docs(file_name=loc,q_link=link)

    elif str(url).endswith(".pdf"):
        loc = f"{loc}.pdf"
        import_docs(file_name=loc, q_link=url)
    elif str(url).endswith(".xlsx"):
        loc = f"{loc}.xlsx"
        import_docs(file_name=loc, q_link=url)
            
    elif loc == "ngs":
        for item in info:
            temp = item.css_first('tbody')
            txts = temp.css('div.container-fluid')
            for txt in txts:
                ans = txt.text(strip=True)
                create_txt(info=ans)
                
    elif loc == "x12":
        info = html.css_first(selector)
        info = info.css('tbody')
        for item in info:
            links = item.css('tr')
            for link in links:
                temp = link.css_first('a')
                file_name = temp.text(strip=True)
                link = temp.attributes['href'].strip()
                link = f"https://x12.org{link}"
                x_data(url=link)
                
    elif loc == "uhc-gen":
        info = html.css_first('div.responsivegrid.leftnav-wrap-border.aem-GridColumn.aem-GridColumn--default--12')
        temps = info.css('a')
        for temp in temps:
            node = temp.css_first('a')
            if node.attributes.__contains__('href') != False:
                if str(node.attributes['href']).startswith("h") == True:
                    link = node.attributes['href']
                    if link not in lst:
                        lst.append(link)
                        if str(link).endswith(".pdf") == True:
                            file_name = node.text(strip=True)
                            file_name = f"{file_name}.pdf"
                            # print(f"full link pdf    {file_name}, {link}")
                            import_docs(file_name=file_name, q_link=link)
                            pass
                        else:
                            # print(f"full link else   {link}")
                            x_data(link)
                elif str(node.attributes['href']).startswith("/") == True:
                    link = node.attributes['href']
                    link = f"https://www.uhcprovider.com{link}"
                    if str(link).endswith(".pdf") == True:
                        file_name = node.text(strip=True)
                        file_name = f"{file_name}.pdf"
                        # print(f"half link pdf    {file_name}, {link}")
                        import_docs(file_name=file_name, q_link=link)
                        pass
                    else:
                        # print(f"half link else   {link}")
                        x_data(link)
            else:
                pass  
    elif loc == "uhc-info":
        
        domain = "https://www.uhc"
        info = html.css_first('div.regioncontainer.responsivegrid.aem-GridColumn--default--none.aem-GridColumn--default--9.aem-GridColumn.aem-GridColumn--offset--default--0')
        t_nodes = info.css('p')
        for t_node in t_nodes:
            text = t_node.css_first('p').text(strip=True)
            # print(text)
            create_txt(text)
        infos = info.css('a')
        for info in infos:
            node = info.css_first('a')
            if node.attributes.__contains__('href') != False:
                    if str(node.attributes['href']).startswith("h") == True:
                        if str(node.attributes['href']).startswith(domain) == True:
                            link = node.attributes['href']
                            if link not in lst:
                                lst.append(link)
                                if str(link).endswith(".pdf") == True:
                                    file_name = node.text(strip=True)
                                    file_name = f"{file_name}.pdf"
                                    # print(f"full link pdf    {file_name}, {link}")
                                    import_docs(file_name=file_name, q_link=link)
                                    pass
                                else:
                                    # print(f"full link else   {link}")
                                    x_data(link)
                        else:
                            pass
                    elif str(node.attributes['href']).startswith("/") == True:
                        link = node.attributes['href']
                        link = f"https://www.uhc.com{link}"
                        if str(link).endswith(".pdf") == True:
                            file_name = node.text(strip=True)
                            file_name = f"{file_name}.pdf"
                            # print(f"half link pdf    {file_name}, {link}")
                            import_docs(file_name=file_name, q_link=link)
                            pass
                        else:
                            # print(f"half link else   {link}")
                            x_data(link)
            else:
                pass
        
            
    elif loc == "uhc":
        title_n = html.css_first('div.rte.component.container.padding.rteAnalytics')
        title = title_n.css_first('p').text(strip=True)
        # print(title)
        create_txt(title)
        nodes = html.css('div.columncontainer.aem-GridColumn--phone--12.aem-GridColumn.aem-GridColumn--default--12')
        for node in nodes:
            p_nodes = node.css('p')
            l_nodes = node.css('a')
            for p_node in p_nodes:
                text = p_node.css_first('p').text(strip=True)
                # print(text)
                create_txt(text)
            for l_node in l_nodes:
                if str(l_node.css_first('a').attributes['href']).endswith('.pdf'):
                    file_name = l_node.text(strip=True)
                    file_name = f"{file_name}.pdf"
                    link = l_node.css_first('a').attributes['href'].strip()
                    link = f"https://www.uhcprovider.com{link}"
                    # print(file_name, link)
                    import_docs(file_name=file_name, q_link=link)
                else:
                    pass
                
    elif loc == "caqh":
        link = html.css_first('div.region.region-content')
        file_name = link.css_first('a').text(strip=True)
        link = link.css_first('a').attributes['href']
        loc = f"{file_name}.xlsx"
        import_docs(file_name=loc, q_link=link)
        

def main():
    results = [
        get_info("Adjustment_codes_carc_rarc", "https://www.aetnabetterhealth.com/content/dam/aetna/medicaid/illinois/providers/pdf/Adjustment_Codes_CARC_and_RARC.pdf", "pdf"),
        print("d1"),
        get_info("provider", "https://provider.bluecrossma.com/ProviderHome/wcm/connect/131578b5-4d88-4060-aab4-5fb6d81392f9/MPC_061317-3H_Correcting_Claims_Rejects.pdf?MOD=AJPERES", "pdf"),
        print("d2"),
        get_info("Claim_Denial_codes", "https://medicaid.utah.gov/Documents/pdfs/ClaimDenialCodes.pdf", "pdf"),
        print("d3"),
        get_info("ngs", "https://www.ngsmedicare.com/claim-errors?lob=93617&state=97227&rgion=93623", "div.content"),
        print("d4"),
        get_info("uhc-gen", "https://www.uhcprovider.com/en/resource-library/edi.html", "div.aem-Grid.aem-Grid--12.aem-Grid--default--12.aem-Grid--phone--12"),
        print("d5"),
        get_info("uhc", "https://www.uhcprovider.com/en/resource-library/edi/edi-smart-edits.html", "div.aem-Grid.aem-Grid--12.aem-Grid--default--12.aem-Grid--phone--12"),
        print("d6"),
        get_info("smart_edits", "https://www.uhcprovider.com/content/dam/provider/docs/public/resources/edi/EDI-ACE-Smart-Edits.pdf", "pdf"),
        print("d7"),
        get_info("Payer-List-UHC", "https://www.uhcprovider.com/content/dam/provider/docs/public/resources/edi/Payer-List-UHC-Affiliates-Strategic-Alliances.pdf", "pdf"),
        print("d8"),
        get_info("caqh", "https://www.caqh.org/core/ongoing-maintenance-core-code-combinations", "div.accordion.ui-accordion.ui-widget.ui-helper-reset"),
        print("d9"),
        get_info("simple", "https://support.simplepractice.com/hc/en-us/articles/360016456811-Resolving-claim-rejections-", "body"),
        print("d10"),
        get_info("CMS", "https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Internet-Only-Manuals-IOMs-Items/CMS018912", "li.field__item"),
        print("d11"),
        get_info("CMS", "https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Internet-Only-Manuals-IOMs-Items/CMS019017", "li.field__item"),
        print("d12"),
        get_info("CMS", "https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Internet-Only-Manuals-IOMs-Items/CMS050111", "li.field__item"),
        print("d13"),
        get_info("uhc-info", "https://www.uhc.com/understanding-health-insurance", "pdf"),
        print("d14"),
        get_info("x12", "https://x12.org/codes", "table.cols-5"),
        print("d15"),
        get_info("Rad_Repository", "https://files.medi-cal.ca.gov/pubsdoco/Publications/masters-MTP/Part1/RAD_Repository.xlsx", "pdf")
    ]

def x_data(url):
    resp = httpx.get(
        url, 
        headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
        }
    )
    html = HTMLParser(resp.content)
    if url == "https://x12.org/codes/property-casualty-code-lists":
        tinfos = html.css_first('div#content-area')#content-area
        tinfos = tinfos.css('div.code_list_accordion__code-list-table')
        for tinfo in tinfos:
            infos = tinfo.css('td')
            for info in infos:
                temp = info.css_first('td').text()        
                create_txt(info=temp)
                # print(temp)
    elif url == "https://x12.org/codes/provider-taxonomy-codes" or str(url).startswith("https://chameleoncloud.io/"):
        pass
    elif url == "https://www.uhcprovider.com/en/resource-library/edi/edi-benefits.html" or url == "https://www.uhcprovider.com/en/resource-library/edi/edi-quick-tips-claims.html":
        text_nodes = html.css('div.accordionitem.panel-default.panel')
        for text_node in text_nodes:
            p_nodes = text_node.css('p')
            for p_node in p_nodes:
                text = p_node.css_first('p').text(strip=True)
                create_txt(text)
                # print(text)
    elif str(url).startswith("https://www.uhcprovider.com") or str(url).startswith("http://www.uhcprovider.com"):
        text_nodes = html.css('div.richtext.text.aem-GridColumn--phone--12.aem-GridColumn--default--9.aem-GridColumn')
        for text_node in text_nodes:
            p_nodes = text_node.css('p')
            for p_node in p_nodes:
                text1 = p_node.css_first('p').text(strip=True)
                create_txt(text1)
                # print(text1)
            b_nodes = text_node.css('li')
            for b_node in b_nodes:
                text2 = b_node.css_first('li').text(strip=True)
                create_txt(text2)
                # print(text2)
    elif url == "https://view-awesome-table.com/-MZTdtM2V0ihM0-nUJKe/view":
        text_nodes = html.css('div.body-child.google-visualization-controls-theme-plus.at-layout-vertical')
        print(text_nodes)
        for text_node in text_nodes:
            nodes = text_node.css_first('div').child
        
            print(nodes)
            
    elif str(url).startswith("https://www.uhc"):
        nodes = html.css('div.responsivegrid.aem-GridColumn.aem-GridColumn--default--12')
        domain = "https://www.uhc"
        for node in nodes:
            p_nodes = node.css('p')
            l_nodes = node.css('a')
            for p_node in p_nodes:
                text = p_node.css_first('p').text(strip=True)
                # print(text)
                create_txt(text)
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
                                    import_docs(file_name=file_name, q_link=link)
                                    pass
                                elif str(link).endswith(".xlsx") == True:
                                    file_name = l_node.text(strip=True)
                                    file_name = f"{file_name}.xlsx"
                                    # print(f"full link pdf    {file_name}, {link}")
                                    import_docs(file_name=file_name, q_link=link)
                                    pass
                                else:
                                    # print(f"full link else   {link}")
                                    x_data(link)
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
                                import_docs(file_name=file_name, q_link=link)
                                pass
                            elif str(link).endswith(".xlsx") == True:
                                file_name = l_node.text(strip=True)
                                file_name = f"{file_name}.xlsx"
                                # print(f"half link pdf    {file_name}, {link}")
                                import_docs(file_name=file_name, q_link=link)
                                pass
                            else:
                                # print(f"half link else   {link}")
                                x_data(link)
                        else:
                            pass
                    else:
                        pass    
            else:
                pass
    else:
        infos = html.css_first('div.code_list__code-list-table')
        infos = infos.css_first('tbody')
        infos = infos.css('td')
        for info in infos:
            temp = info.css_first('td').text(strip=True)
            create_txt(info=temp)
    
    
def import_docs(file_name, q_link):
    if file_name.__contains__("/"):
        file_name = str(file_name).replace("/", "-")
    #location of directory to save files
    output_dir = '.\data'
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
    
    
    
if __name__ == "__main__":
    main()