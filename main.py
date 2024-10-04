from flet import *
import requests
from bs4 import BeautifulSoup

res = requests.get(f"https://www.yallakora.com/match-center")
src = res.content
soup = BeautifulSoup(src , "lxml")

chamption = soup.find_all("div" , {"class" : "matchCard"})
mat = []

def main(page : Page):
    page.scroll = 'auto'
    page.rtl = True
    page.window_height = 1050
    page.window_width = 2800
    page.window_center()
    
    def back(e , route):
        page.clean()
        if route == "main":
            main(page)
        elif route == "fplhome":
            fplhome(e)
        elif route =="pages":
            pages(e)
        
    def matches(e):
        page.clean()
        page.add(
                Container(content=Row(
                                    [
                                        ElevatedButton("Back", width=100 , on_click=lambda e: back(e , "main"), bgcolor=colors.BLACK87 , color=colors.AMBER),
                                    ],
                                    alignment=MainAxisAlignment.CENTER
                                ),
                ))
        def get(chamption) : 
            chamption_title = chamption.contents[1].find("h2").text.strip()
            all = chamption.contents[3].find_all("div" , {"class":"item"})
            num = len(all)
            for i in range(num):
                date = all[i].find("div" , {"class":"date"}).text.strip()
                channel = all[i].find("div" , {"class":"channel"})
                state = all[i].find("span").text.strip()
                resl = all[i].find("div" , {"class" : "MResult"}).find_all("span" , {"class" : "score"})
                reslt = f"{resl[0].text.strip()} - {resl[1].text.strip()}"
                clock = all[i].find("div" , {"class" : "MResult"}).find("span" , {"class" : "time"}).text.strip()
                # global teamA
                teamA = all[i].find("div" , {"class":"teamA"}).text.strip()
                teamB = all[i].find("div" , {"class":"teamB"}).text.strip()
                pen = all[i].find("div" , {"class" : "MResult"}).find("div" , {"class" : "penaltyRes"})
                # print(pen)
                if pen == None:
                    pass
                else:
                    reslt = reslt + f"  {pen.text.strip()}"
                
                if channel == None:
                    channel = "غير مذاع"
                else:
                    channel = all[i].find("div" , {"class":"channel"}).text.strip()
                panel1 =  ExpansionPanelList(
                    expand_icon_color= colors.AMBER,
                    elevation=8,
                    divider_color= colors.AMBER,
                    controls=[
                        ExpansionPanel(
                            header= ListTile(title= Text("تفاصيل")),
                            content=(Container(
                                content=Column(expand=True , controls=[Column([Text(f"الحاله :  {state}")]), Column([Text(f"الحاله :  {channel}")]) , Column([Text(f"الاسبوع / الدور :  {date}")]) , Column([Container(content=Text(f"التوقيت :  {clock}") ,padding=padding.only(bottom=10) )])]),
                                padding=padding.all(5)
                                )
                            )
                        )
                    ]
                )
                page.add(
                    Container(
                        alignment=alignment.center,
                            content=Card(
                                content=Container(
                                    content=Column(
                                        [
                                            ListTile(
                                                title=Container(content=Text(chamption_title) , padding=padding.only(bottom=5)),
                                                subtitle=Container(
                                                    content=Row(
                                                        [Text(
                                                    teamA + f"  {reslt}  "+teamB
                                                )], alignment=MainAxisAlignment.CENTER , vertical_alignment=CrossAxisAlignment.CENTER), alignment=alignment.center),
                                            ),
                                            panel1
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    width=700,
                                    padding=16,
                                    alignment=alignment.center,
                                )
                            )
                    )
                )
        for i in range(len(chamption)) :
            get(chamption[i])
    
    
    def FPL(e):
        page.clean()
        ID = TextField(label="Your ID" , input_filter=NumbersOnlyInputFilter() , border_color=colors.BLACK , border_width=2  , show_cursor=False ,color=colors.WHITE , rtl=False , text_align=TextAlign.LEFT , label_style = TextStyle(color=colors.BLACK))
        players_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

        p = requests.get(players_url)
            
        Players_data = p.json()
            
        def team(e):
                    name = ID.value
                    manger = f"https://fantasy.premierleague.com/api/entry/{name}"
                    ru = requests.get(manger)
                    manger_data = ru.json()
                    ev = manger_data['current_event']
                    picks = f"https://fantasy.premierleague.com/api/entry/{name}/event/{ev}/picks/"
                    r = requests.get(picks)
                    picks_data = r.json()
                    tt=[]
                    for i in picks_data['picks']:
                        for u in Players_data['elements']:
                            if u['id'] == i['element']:
                                if i['multiplier'] == 0:
                                    continue
                                if i['multiplier'] == 2:
                                    tt.append(u['event_points'] *2)
                                    continue
                                tt.append(u['event_points'])
                                    
                    page.clean()
                    
                    # Bacl
                    page.add(
                        Container(
                            content=ElevatedButton("Back", on_click=lambda e: back(e , "pages") , width=100 , color=colors.AMBER),
                            padding=padding.only(top=18 , bottom=10),
                            alignment=alignment.center,
                            # width=400
                        ),
                    )
                    # Name
                    page.add(
                        Container(alignment=alignment.center,
                            content=Card(
                                            content=Container(
                                                content=Column(
                                                    [
                                                        ListTile(
                                                            title=Container(content=Column(
                                                                controls=[
                                                                    Row(controls=[Text(Text(f"{manger_data['player_first_name']} {manger_data['player_last_name']}" , size=32)).value] , alignment=MainAxisAlignment.CENTER),
                                                                    Row(controls=[Text(Text(f"{manger_data['name']}" , size=32)).value] , alignment=MainAxisAlignment.CENTER)
                                                                ]    
                                                            ) , alignment=alignment.center),
                                                            subtitle = Container(content=Text(f"Rank: {manger_data['summary_overall_rank']}" , size=14) , alignment=alignment.center),
                                                            title_alignment=ListTileTitleAlignment.CENTER,
                                                            horizontal_spacing =2
                                                        ),
                                                        Row(
                                                            [Text(
                                                                f"Points: {picks_data['entry_history']['points']}",
                                                                size=25,
                                                            )],
                                                            alignment=MainAxisAlignment.CENTER,
                                                        ),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                                ),
                                                border=border.all(1 , colors.AMBER),
                                                width=450,
                                                padding=10,
                                                gradient=LinearGradient(
                                                    begin=alignment.bottom_left,
                                                    end=alignment.top_right,
                                                    colors=["#1e293b" , "#475569"]
                                                ),
                                                border_radius=15,alignment=alignment.center
                                            )
                                        )

                        )
                    )
                    # Start
                    page.add(
                        Container(
                            content=Row(
                            [
                                Text("START" , size=20),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            width=450
                        ),
                            alignment=alignment.center,
                        )
                    )
                    for i in picks_data['picks']:
                        for u in Players_data['elements']:
                            if u['id'] == i['element'] and (i['multiplier'] == 1 or i['multiplier'] == 2):
                                imga = u['photo'][:-4]
                                if i['multiplier'] == 2:
                                    page.add(
                                        Container(alignment=alignment.center,
                                            content=Card(
                                            content=Container(
                                                content=Column(
                                                    [
                                                        ListTile(
                                                            leading=Icon(icons.CYCLONE_ROUNDED),
                                                            title=Image(src=f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{imga}.png" , width=250 , height=250),
                                                            title_alignment=alignment.center,
                                                            horizontal_spacing =2
                                                        ),
                                                        Row(
                                                            [Text(
                                                                u['web_name'],
                                                                size=40,
                                                            )],
                                                            alignment=MainAxisAlignment.CENTER,
                                                        ),
                                                        Row(
                                                            [Text(
                                                                f"{u['event_points'] * 2}  |  {u['now_cost'] / 10}",
                                                                size=30,
                                                            )],
                                                            alignment=MainAxisAlignment.CENTER,
                                                        ),
                                                    ]
                                                ),
                                                width=450,
                                                padding=10,
                                                gradient=LinearGradient(
                                                    begin=alignment.bottom_left,
                                                    end=alignment.top_right,
                                                    colors=["#1e293b" , "#475569"]
                                                ),
                                                border_radius=15,
                                                alignment=alignment.center
                                            )
                                        )

                                        )
                                    )
                                    continue
                                page.add(
                                    Container(
                                        alignment=alignment.center,
                                        content=Card(
                                            content=Container(
                                                content=Column(
                                                    [
                                                        ListTile(
                                                            # leading=Icon(icons.CYCLONE_ROUNDED),
                                                            title=Image(src=f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{imga}.png" , width=250 , height=250),
                                                            title_alignment=alignment.center,
                                                            horizontal_spacing =2
                                                        ),
                                                        Row(
                                                            [Text(
                                                                u['web_name'],
                                                                size=40,
                                                                style=TextThemeStyle.HEADLINE_SMALL
                                                            )],
                                                            alignment=MainAxisAlignment.CENTER,
                                                        ),
                                                        Row(
                                                            [Text(
                                                                f"{u['event_points']}  |  {u['now_cost'] / 10}",
                                                                size=30,
                                                                
                                                            )],
                                                            alignment=MainAxisAlignment.CENTER,
                                                        ),
                                                    ]
                                                ),
                                                width=450,
                                                padding=10,
                                                gradient=LinearGradient(
                                                    begin=alignment.bottom_left,
                                                    end=alignment.top_right,
                                                    colors=["#1e293b" , "#475569"]
                                                ),
                                                border_radius=15
                                            )
                                        )
 
                                    )
                                )
                                page.update()
                    
                    page.add(
                        Container(
                            alignment=alignment.center,
                            content=Row(
                            [
                                Text("Substiutes" , size=20),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            width=500
                        )
                        )
                    )
                    for i in picks_data['picks']:
                        for u in Players_data['elements']:
                            if u['id'] == i['element'] and i['multiplier'] == 0:
                                imga = u['photo'][:-4]
                                page.add(
                                    Container(
                                        alignment=alignment.center,
                                        content=Card(
                                        content=Container(
                                            content=Column(
                                                [
                                                    ListTile(
                                                        leading=Icon(icons.HIDE_SOURCE_OUTLINED),
                                                        title=Image(src=f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{imga}.png" , width=250 , height=250),
                                                        title_alignment=alignment.center,
                                                        horizontal_spacing =2
                                                    ),
                                                    Row(
                                                        [Text(
                                                            u['web_name'],
                                                            size=40,
                                                        )],
                                                        alignment=MainAxisAlignment.CENTER,
                                                    ),
                                                    Row(
                                                        [Text(
                                                            f"{u['event_points']}  |  {u['now_cost'] / 10}",
                                                            size=30,
                                                        )],
                                                        alignment=MainAxisAlignment.CENTER,
                                                    ),
                                                ]
                                            ),
                                            width=450,
                                            padding=10,
                                            gradient=LinearGradient(
                                                begin=alignment.bottom_left,
                                                end=alignment.top_right,
                                                colors=["#1e293b" , "#475569"]
                                            ),
                                            border_radius=15,alignment=alignment.center
                                        )
                                    )
                                    )
                                )
                                page.update()
                    
        def leauge(e):
                    page.clean()
                    name = ID.value
                    manger = f"https://fantasy.premierleague.com/api/entry/{name}"
                    ru = requests.get(manger)
                    manger_data = ru.json()
                    page.clean()
                    page.add(
                                Container(

                                    content=ElevatedButton("Back", on_click=lambda e: back(e , "pages") , width=100 , color=colors.AMBER),
                                    padding=padding.only(top=18 , bottom=10),
                                    alignment=alignment.center,
                                    # width=400
                                ),
                    )
                    page.add(
                        Container(
                            alignment=alignment.center
                            ,content=Card(
                                                    content=Container(
                                                        content=Column(
                                                            [
                                                                ListTile(
                                                                    title=Container(content=Column(
                                                                    controls=[
                                                                        Row(controls=[Text(Text(f"{manger_data['player_first_name']} {manger_data['player_last_name']}" , size=32)).value] , alignment=MainAxisAlignment.CENTER),
                                                                        Row(controls=[Text(Text(f"{manger_data['name']}" , size=32)).value] , alignment=MainAxisAlignment.CENTER)
                                                                    ]    
                                                            ) , alignment=alignment.center),
                                                                    subtitle = Container(content=Text(f"Rank: {manger_data['summary_overall_rank']}" , size=14) , alignment=alignment.center),
                                                                    title_alignment=ListTileTitleAlignment.CENTER,
                                                                    horizontal_spacing =2
                                                                ),
                                                            ],
                                                            alignment=MainAxisAlignment.CENTER,
                                                            horizontal_alignment=CrossAxisAlignment.CENTER
                                                        ),
                                                        border=border.all(1 , colors.AMBER),
                                                        width=500,
                                                        padding=10,
                                                        gradient=LinearGradient(
                                                            begin=alignment.bottom_left,
                                                            end=alignment.top_right,
                                                            colors=["#1e293b" , "#475569"]
                                                        ),
                                                        border_radius=15,
                                                        alignment=alignment.center,
                                                    )
                                                )
 
                        )
                    )

                    for i in manger_data['leagues']['classic']:
                            standingsURl = f"https://fantasy.premierleague.com/api/leagues-classic/{i['id']}/standings"
                            rsc = requests.get(standingsURl)
                            Standings = rsc.json()
                            panel2 =  ExpansionPanelList(
                    expand_icon_color= colors.AMBER,
                    elevation=8,
                    divider_color= colors.AMBER,
                    controls=[
                        ExpansionPanel(
                                    header= ListTile(title= Text("تفاصيل")),
                                    content=Container(
                                        expand=True,
                                        content=Column(expand=True), padding=padding.only(bottom=20)),
                                    # expanded=True,
                                )
                            ]
                        )
                            panel2.controls[0].content.content.controls.append(Column([Text(f"Player Name    Total" , size=20 , text_align=TextAlign.RIGHT)]))
                            for y in Standings['standings']['results']:
                                if y['rank'] <= 10:
                                    # print(f"{y['player_name']} {y['total']}")
                                    panel2.controls[0].content.content.controls.append(Container( content=Column([Text(f"{y["player_name"]}    {y["total"]}" , text_align=TextAlign.RIGHT)])))
                                    
                            page.add(
                                Container(
                                    alignment=alignment.center
                                    ,content=Card(
                                content=Container(
                                    alignment=alignment.center,
                                    content=Column(
                                        alignment=MainAxisAlignment.CENTER,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
                                            ListTile(
                                                leading=Icon(icons.SPORTS_SOCCER_OUTLINED),
                                                title=Container(alignment=alignment.center , content=Text(i['name'] , size=30)),
                                                subtitle=Container(alignment=alignment.center , content=Text(
                                                    f"Rank : {i['entry_rank']}" , size=13
                                                )),
                                                title_alignment=alignment.center,
                                            ),
                                            panel2
                                        ]
                                    ),
                                    width=500,
                                    padding=10,
                                    gradient=LinearGradient(
                                        begin=alignment.bottom_left,
                                        end=alignment.top_right,
                                        colors=["#1e293b" , "#475569"]
                                    ),
                                    border_radius=15
                                ),
                            )

                                )
                            )
                    page.update()
        global pages
        def pages(e):
            if ID.value =='':
                fplhome(e)
                ID.error_text = "Please enter your ID"
                page.update()
            else:
                page.clean()
                c = Container(
                        content=Column(

                            controls=[
                                Column(
                            horizontal_alignment=CrossAxisAlignment.START,
                            controls=[
                                        
                                        Row(
                                            [
                                                ElevatedButton("Back", on_click=lambda e: back(e , "fplhome") , width=100 , color=colors.AMBER)                                
                                            ],
                                            alignment=MainAxisAlignment.CENTER,
                                            vertical_alignment= CrossAxisAlignment.START
                                        )
                            ],
                            
                        ),
                                        
                                Column(
                                    [
                                        Row(
                                            [
                                                ElevatedButton(content=Text("نقاط الفريق" , size=20), on_click=team , width=350 , height=100 , bgcolor=colors.BLACK87 , color=colors.AMBER)
                                            ],
                                            alignment=MainAxisAlignment.CENTER
                                        ),
                                        Row(
                                            [
                                                ElevatedButton(content=Text("الدوريات" , size=20), on_click=leauge , width=350 , height=100 , bgcolor=colors.BLACK87 , color=colors.AMBER)
                                            ],
                                            alignment=MainAxisAlignment.CENTER
                                        ),
                                    ]
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,                            
                        ),
                        image_src="zigzag-blue-background-epl-english-premier-league-thumbnail-video-print-web-background-free-vector.jpg",
                        height = 1000,
                    )
                page.add(c)
                
                
        global fplhome        
        def fplhome(e):
            page.add(
            Container(
                content=Column(controls=[
                    Container(
                    Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Row(
                                            [
                                                ElevatedButton("Back", on_click=lambda e: back(e , "main") , width=100 , color=colors.AMBER)                                
                                            ],
                                            alignment=MainAxisAlignment.CENTER
                                        ),
                                    Row(
                                        [
                                            ID
                                        ],
                                        alignment=MainAxisAlignment.CENTER
                                    ),
                                    Row(
                                        [
                                            ElevatedButton("التالى" , width=300 , height=40 , bgcolor=colors.BLACK87 , color=colors.AMBER , on_click=pages)
                                        ],
                                        alignment=MainAxisAlignment.CENTER
                                    ),
                        ],
                    ),
                    image_src="zigzag-blue-background-epl-english-premier-league-thumbnail-video-print-web-background-free-vector.jpg",
                    alignment=alignment.center,
                    height = 1000,
                )

                ])
            )
        )
        page.update()
        fplhome(e)
            
    page.add(
        Container(
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER
                ,controls=[
                    Container(
                        content=Row(
                        [
                            ElevatedButton(content=Text("جدول المباريات" , size=20), on_click=matches, width=300 , height=100 , bgcolor=colors.BLACK87 , color=colors.AMBER)
                        ],
                        alignment=MainAxisAlignment.CENTER
                        ),
                    ),
                    Container(
                        content=Row(
                        [
                            ElevatedButton(content=Text("فانتازى الدورى الانجليزى" , size=20),on_click=FPL , width=300 , height=100 , bgcolor=colors.BLACK87 , color=colors.AMBER)
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                    )
                ]
            ),
            image_src="jannes-glas-cuhQcfp3By4-unsplash.jpg",
            image_fit=ImageFit.CONTAIN,
            height=1000,
        )
    )
    
    
    
    
if __name__ == "__main__":
    app(main , assets_dir="assets")