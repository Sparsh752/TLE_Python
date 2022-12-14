from bs4 import BeautifulSoup
import requests
import asyncio

### checks just completed contest

async def completed_contest(html_):
    soup1 = BeautifulSoup(html_,'html.parser')
    for el in soup1.find_all("tr"):
        if el.has_attr("data-contestid"):
            contest_ID=el.attrs["data-contestid"]
            break
    return contest_ID


async def print_final_standings(): 
    print('YES') 


#### If rating changes came then show standing 
async def show_standings():
    while(1):
        await asyncio.sleep(60)
        # bool_ -> Last contest final standings arrived or not..
        bool_ = await check_rating_changed('1764')
        if(bool_):
            await print_final_standings()
        else:
            print('NO')


### checks if rating changes arrived

async def check_rating_changed(previous_contestId):
    url = "https://codeforces.com/contests"
    r = requests.get(url)   
    soup = BeautifulSoup(r.content, 'html.parser')  
    s = soup.find('div', class_= 'contests-table')  
    _html=str(s)
    contest_id= await completed_contest(_html)
    if(contest_id==previous_contestId):          # if contest updates already given then end func
        return False
    else:
        s1= soup.find('a', href= '/contest/'+str(contest_id)+'/standings')
        nlist = s1.text
        if 'Final standings' in nlist:
            url = ('https://codeforces.com/contest/'+str(contest_id)+'/standings')
            r = requests.get(url)  
            soup = BeautifulSoup(r.content, 'html.parser')  
            
            s = soup.find('div', class_= 'second-level-menu')  
            nlist = s.text
            if "Rating Changes" in nlist:
                print("yes rating changes came")



                #### Update previous contest Id in Firebase with ((( contest_id )))  #######



                return True
            else:
                return False

        else:
            return False