from textblob import TextBlob
from flask import Flask
from flask import request
from flask import render_template
from bs4 import BeautifulSoup 
import requests
import praw
import tweepy,re

overall_report=[]
facebook_Report=[]
reddit_Report=[]
twitter_Report=[]
news_Report=[]
instagram_Report=[]


facebook_dataset=[]
twitter_dataset=[]
instagram_dataset=[]
reddit_dataset=[]
news_db=[]

fb_chart=[]
tw_chart=[]
rd_chart=[]
in_chart=[]
nw_chart=[]




app = Flask(__name__,template_folder='./template',static_url_path='/static')
@app.route('/')
def my_form():
    return render_template("fon.html")
    


class SentimentAnalysis:
        def __init__(self):
            self.tweets = []
            self.tweetText = []
        def twitter(self,st):
                sa = SentimentAnalysis()
                # authenticating
                consumerKey = ''
                consumerSecret = ''
                accessToken = ''
                accessTokenSecret = ''
                auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
                auth.set_access_token(accessToken, accessTokenSecret)
                api = tweepy.API(auth)
                
                # input for term to be searched and how many tweets to search
                searchTerm = str(st)
                
                NoOfTerms = 100
                # searching for tweets
                self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
                # creating some variables to store info
                polarity = 0
                positive = 0
                wpositive = 0
                spositive = 0
                negative = 0
                wnegative = 0
                snegative = 0
                neutral = 0

                
                # iterating through tweets fetched
                for tweet in self.tweets:
                    #Append to temp so that we can store in csv later. I use encode UTF-8
                    self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                    #print (tweet.text)    #print tweet's text( Twitter data)
                    analysis = TextBlob(tweet.text)
                    twitter_dataset.append(tweet.text)

                tw_hash = requests.get("https://www.hashatit.com/hashtags/"+ searchTerm +"/twitter")
                tw_soup = BeautifulSoup(tw_hash.text, "html.parser")
                resultDiv = tw_soup.find_all('div', attrs = {'class' : 'media-box-text'})
                for r in resultDiv:
                    try:
                        twitter_dataset.append(r.get_text())
                    except:
                        continue
                sa.do_nlp(twitter_dataset,"Twitter",len(twitter_dataset),searchTerm,twitter_Report,tw_chart)

                

 
        def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

        def percentage(self, part, whole):
            try:
                temp = 100 * float(part) / float(whole)
                return format(temp, '.2f')
            except:
                return format(0,'.2f')

        def do_nlp(self,data,src,count,key,Report,chart,):
                # creating some variables to store info
                
                    print(" count got is ---->>  ")
                    print(count)

                    
                    polarity = 0
                    positive = 0
                    wpositive = 0
                    spositive = 0
                    negative = 0
                    wnegative = 0
                    snegative = 0
                    neutral = 0
                    NoOfTerms=count
                    for datum in data[:]:
                        # print (tweet.text.translate(non_bmp_map))    #print tweet's text
                        analysis = TextBlob(datum)
                        
                        # print(analysis.sentiment)  # print tweet's polarity
                        polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

                        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                            neutral += 1
                        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                            wpositive += 1                                  
                        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                            positive += 1
                        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                            spositive += 1
                        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                            wnegative += 1
                        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                            negative += 1
                        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                            snegative += 1
                        
                    # finding average of how people are reacting
                    positive = self.percentage(positive, NoOfTerms)
                    wpositive = self.percentage(wpositive, NoOfTerms)
                    spositive = self.percentage(spositive, NoOfTerms)
                    negative = self.percentage(negative, NoOfTerms)
                    wnegative = self.percentage(wnegative, NoOfTerms)
                    snegative = self.percentage(snegative, NoOfTerms)
                    neutral = self.percentage(neutral, NoOfTerms)
                    
                    # finding average reaction
                    try:
                        polarity = polarity / NoOfTerms
                    except :
                        polarity = 0
                   # print(positive)
                    #print(wpositive)
                    # printing out data
                    print("How people are reacting on "+ key +" by analyzing")

                    Report.append("How people are reacting on "+ key + " by analyzing " + src)
                    
                    
                    
                    print("General Report: ")
                    Report.append("General Report")
                   
                    if (polarity == 0):
                        print("Neutral")
                        Report.append("Neutral")
                    elif (polarity > 0 and polarity <= 0.3):
                        print("Weakly Positive")
                        Report.append("Weakly Positive")
                    elif (polarity > 0.3 and polarity <= 0.6):
                        print("Positive")
                        Report.append("Positive")
                    elif (polarity > 0.6 and polarity <= 1):
                        print("Strongly Positive")
                        Report.append("Strongly Positive")
                    elif (polarity > -0.3 and polarity <= 0):
                        print("Weakly Negative")
                        Report.append("Weakly Negative")
                    elif (polarity > -0.6 and polarity <= -0.3):
                        print("Negative")
                        Report.append("Negative")
                    elif (polarity > -1 and polarity <= -0.6):
                        print("Strongly Negative")
                        Report.append("Strongly Negative")

                    print("Detailed Report: ")
                    Report.append("Detailed Report: ")
                    print(str(positive) + "% people thought it was positive")
                    Report.append(str(positive) + "% people thought it was positive")
                    print(str(wpositive) + "% people thought it was weakly positive")
                    Report.append(str(wpositive) + "% people thought it was weakly positive")
                    print(str(spositive) + "% people thought it was strongly positive")
                    Report.append(str(spositive) + "% people thought it was strongly positive")
                    print(str(negative) + "% people thought it was negative")
                    Report.append(str(negative) + "% people thought it was negative")
                    print(str(wnegative) + "% people thought it was weakly negative")
                    Report.append(str(wnegative) + "% people thought it was weakly negative")
                    print(str(snegative) + "% people thought it was strongly negative")
                    Report.append(str(snegative) + "% people thought it was strongly negative")
                    print(str(neutral) + "% people thought it was neutral")
                    Report.append(str(neutral) + "% people thought it was neutral")
                    print("\n")

                    chart.append(float(positive))
                    chart.append(float(wpositive))
                    chart.append(float(spositive))
                    chart.append(float(negative))
                    chart.append(float(wnegative))
                    chart.append(float(snegative))
                    chart.append(float(neutral))
                    print('\n')  

        def facebook(self,search):
            sa = SentimentAnalysis()
            fb_hash = requests.get("https://www.hashatit.com/hashtags/"+ search +"/facebook")
            fb_soup = BeautifulSoup(fb_hash.text, "html.parser")
            resultDiv = fb_soup.find_all('div', attrs = {'class' : 'media-box-text'})

            for r in resultDiv:
                try:
                    facebook_dataset.append(r.get_text())
                except:
                    continue
            if len(facebook_dataset)==0:   
                for i in range(0,10):
                    facebook_Report.append("Data Not Available")
                for i in range(0,7):
                    fb_chart.append(0.0)
            else:
                sa.do_nlp(facebook_dataset,"Facebook",len(facebook_dataset),search,facebook_Report,fb_chart)

        def reddit(self,search):
            sa = SentimentAnalysis()
            reddit_client_id = 'eGO3BN826LwxtQ'
            reddit_client_secret = 	'W4jB3kbhM-1xpbV8cUoAR5NGWMI'
            username = 'amrcoder1155@gmail.com'
            password = 'anish1997'
            user_agent = 'my user agent'  
            reddit = praw.Reddit(client_id = reddit_client_id, client_secret = reddit_client_secret, user_agent = user_agent) #reddit api data
            try:
                for i in reddit.subreddit(search).hot(limit=50):
                    reddit_dataset.append(i.selftext)
            except :
                pass
            if len(reddit_dataset)==0:   
                for i in range(0,10):
                    reddit_Report.append("Data Not Available")
                for i in range(0,7):
                    rd_chart.append(0.0)
            else:
                sa.do_nlp(reddit_dataset,"Reddit",len(reddit_dataset),search,reddit_Report,rd_chart)

        def instagram(self,search):
            sa = SentimentAnalysis()
            in_hash = requests.get("https://www.hashatit.com/hashtags/"+ search +"/instagram")
            in_soup = BeautifulSoup(in_hash.text, "html.parser")
            resultDiv = in_soup.find_all('div', attrs = {'class' : 'media-box-text'})
            for r in resultDiv:
                try:
                    instagram_dataset.append(r.get_text())
                except:
                    continue
            if len(instagram_dataset)==0:   
                for i in range(0,10):
                    instagram_Report.append("Data Not Available")
                for i in range(0,7):
                    in_chart.append(0.0)
            else:
                sa.do_nlp(instagram_dataset,"Instagram",len(instagram_dataset),search,instagram_Report,in_chart)

        def keyword(self,search):
            
            keyword = requests.get("https://www.hashatit.com/keyword/" + search )
            soup = BeautifulSoup(keyword.text, "html.parser")
            resultDiv = soup.find_all('div', attrs = {'class' : 'media-box-text'})
            for r in resultDiv:
                try:
                    instagram_dataset.append(r.get_text())
                    twitter_dataset.append(r.get_text())
                    facebook_dataset.append(r.get_text())
                except:
                    continue

        def news(self,search):
            sa = SentimentAnalysis()
            for i in range(1,3):
                        news = requests.get("https://www.news18.com/newstopics/"+ search +"/news/page-"+str(i)+"/")

                        nw_soup = BeautifulSoup(news.text,'html.parser')

                        resultDiv = nw_soup.find_all('h2')

                        for r in resultDiv:
                            try:
                                #print(r)
                                news_db.append(r.get_text())
                            except:
                                continue


                        resultDiv = nw_soup.find_all('p')
                        for r in resultDiv:
                            try:
                            # print(r)
                                news_db.append(r.get_text())
                            except: 
                                continue


            if len(news_db)==0:   
                for i in range(0,10):
                    news_Report.append("Data Not Available")
                for i in range(0,7):
                    nw_chart.append(0.0)
            else:              
                sa.do_nlp(news_db,"NEWS18",len(news_db),search,news_Report,nw_chart)


def run_focus(search):
    
    sa = SentimentAnalysis()

    print('keyword')
    sa.keyword(search)

    print('twitter')
    sa.twitter(search)

    print('fb')
    sa.facebook(search)   
    
    print('reddit')
    sa.reddit(search)
    
    print('instagram')
    sa.instagram(search)

    print('news')
    sa.news(search)


@app.route('/getvalue', methods=['POST'])
def getvalue():
    search=request.form['option']
    print(search)
    run_focus(search)

    overall_chart=[]
    overall_report=[]
    for i in range(0,7):
        overall_chart.append(round((tw_chart[i]+nw_chart[i]+rd_chart[i]+fb_chart[i]+in_chart[i])/5,2))
    del overall_chart[-1]
    print(overall_chart)
    
    maxy=overall_chart.index(max(overall_chart))

    overall_report.append("Over all report on How people are reacting on "+ search)
    overall_report.append("General Report")
    if(maxy==0):
        overall_report.append("Positive")
    elif (maxy==1):
        overall_report.append("Weakly positive")
    elif (maxy==2):
        overall_report.append("Strongly positive")
    elif (maxy==3):
        overall_report.append("Negative")
    elif (maxy==4):
        overall_report.append("Weakly negative")
    elif (maxy==5):
        overall_report.append("Strongly negative")
    #elif (maxy==6):
    #    overall_report.append("Neutral")

    overall_report.append("Detailed Report")
    overall_report.append( str(overall_chart[0]) + "% people thought it was positive")
    overall_report.append( str(overall_chart[1]) + "% people thought it was weakly positive")
    overall_report.append( str(overall_chart[2]) + "% people thought it was strongly positive")
    overall_report.append( str(overall_chart[3]) + "% people thought it was negative")
    overall_report.append( str(overall_chart[4]) + "% people thought it was weakly negative")
    overall_report.append( str(overall_chart[5]) + "% people thought it was strongly negative")
    #overall_report.append( str(overall_chart[6]) + "% people thought it was neutral")


    return render_template('%s.html' % "rs",facebook_Report=facebook_Report,
    facebook_data=facebook_dataset,reddit_Report=reddit_Report,reddit_data=reddit_dataset,
    twitter_Report=twitter_Report,twitter_data=twitter_dataset,fb_chart=fb_chart,
    tw_chart=tw_chart,rd_chart=rd_chart,instagram_Report=instagram_Report,
    instagram_data=instagram_dataset,in_chart=in_chart,news_data=news_db,
    news_Report=news_Report,nw_chart=nw_chart,overall_chart=overall_chart,overall_report=overall_report  )
    
@app.route('/searchvalue', methods=['POST'])
def searchvalue():
    search = request.form['search']
    print(search)
    run_focus(search)

    overall_chart=[]
    overall_report=[]
    for i in range(0,7):
        overall_chart.append(round((tw_chart[i]+nw_chart[i]+rd_chart[i]+fb_chart[i]+in_chart[i])/5,2))
    maxy=overall_chart.index(max(overall_chart))
    overall_report.append("Over all report on How people are reacting on "+ search)
    overall_report.append("General Report")
    if(maxy==0):
        overall_report.append("Positive")
    elif (maxy==1):
        overall_report.append("Weakly positive")
    elif (maxy==2):
        overall_report.append("Strongly positive")
    elif (maxy==3):
        overall_report.append("Negative")
    elif (maxy==4):
        overall_report.append("Weakly negative")
    elif (maxy==5):
        overall_report.append("Strongly negative")
    elif (maxy==6):
        overall_report.append("Neutral")

    overall_report.append("Detailed Report")
    overall_report.append( str(overall_chart[0]) + "% people thought it was positive")
    overall_report.append( str(overall_chart[1]) + "% people thought it was weakly positive")
    overall_report.append( str(overall_chart[2]) + "% people thought it was strongly positive")
    overall_report.append( str(overall_chart[3]) + "% people thought it was negative")
    overall_report.append( str(overall_chart[4]) + "% people thought it was weakly negative")
    overall_report.append( str(overall_chart[5]) + "% people thought it was strongly negative")
    overall_report.append( str(overall_chart[6]) + "% people thought it was neutral")
    
    


    return render_template('%s.html' % "rs",facebook_Report=facebook_Report,
    facebook_data=facebook_dataset,reddit_Report=reddit_Report,reddit_data=reddit_dataset,
    twitter_Report=twitter_Report,twitter_data=twitter_dataset,fb_chart=fb_chart,
    tw_chart=tw_chart,rd_chart=rd_chart,instagram_Report=instagram_Report,
    instagram_data=instagram_dataset,in_chart=in_chart,news_data=news_db,
    news_Report=news_Report,nw_chart=nw_chart,overall_chart=overall_chart,overall_report=overall_report)
    


if __name__== "__main__":
    app.run()
    #run_focus("IndianRailway")
    sa = SentimentAnalysis()
