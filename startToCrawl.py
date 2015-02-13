import getSongs
import curieCrawler

crawlOrder = ["Bugs", "Melon", "Navermusic", "Youtube"] # Your crawling follow this order

filename = getSongs.start(8,1,0) # 1 to 8 for each machine

for i in range(len(crawlOrder)):
	c = curieCrawler.Crawler(filename)
	filename = c.scrapFrom(crawlOrder[i])

# Total 10 columns in final created CSV file
