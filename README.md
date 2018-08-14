# Billboard Songs

Creates a new playlist with Top 50 songs from "Billboard Songs" list

### Prerequisites
1. Create an account on https://developer.spotify.com/
2. Get your Client Id, Client Secret and Redirect Uri


### Installing
```
git clone https://github.com/ansonj712/Billboard-Songs.git
pip install -r requirements.txt
```

### How to Use
1. Edit the config.py file with your Client Id, Client Secret, Redirect Uri, 
and Account

2. Get the URL of the chart
then run the following command
```
python run.py https://www.billboard.com/charts/dance-electronic-songs
```