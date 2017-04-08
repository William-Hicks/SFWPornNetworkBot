import praw
import time 
import threading 
import re
import os
import datetime
import PIL
import sys
import html.parser
import PIL.Image
import PIL.ExifTags
import urllib.request
import urllib.request as request


os.system('chcp 65001')
multi = ['EarthPorn','MilitaryPorn','QuotesPorn']

regular_flairs = 'private PrivateFirstClass Specialist Coporal Sergeant StaffSergeant SergeantFirstClass MasterSergeant 2ndLT 1stLt Captain Major LTColonel BrigadierGeneral MajorGeneral LTGeneral General'
flairs = list(regular_flairs.split())

class Image(object):

	def __init__(self, submission, subreddit):
		time.sleep(60)
		print('Checking image on /r/{}'.format(subreddit))
		self.submission = submission
		self.title = submission.title
		self.permalink = submission.permalink
		self.url = submission.url
		self.author = submission.author
		self.id = submission.id
		self.subreddit = subreddit
		self.run()

	def submit_to_database(self):
		with open('database.txt','a') as db:
			db.write(str(self.id) + '\n')
			db.close()
			print('Saved to database!')

	def check_database(self):
		with open('database.txt','r') as db:
			file = db.read()
			if str(self.id) not in file:
				return True
			else:
				return False

	def __image__(self):
		image = urllib.request.urlretrieve(self.url,'C:/Users/whick/Subreddit/image.jpg')
		with PIL.Image.open('image.jpg') as img:
			width, height = img.size
		image_size = '[{}x{}]'.format(width, height)
		return(image_size)

	def check_title(self):
		try:
			size = str(self.title)[re.search('\[',str(self.title)).span()[1]:re.search('\]',str(self.title)).span()[0]]
			size = str(' '.join(re.findall('\d+(?:\.\d+)?', size)))
			image_size = str(' '.join(re.findall('\d+(?:\.\d+)?',str(self.__image__()))))
			image_size = image_size.replace(' ','x')
			image_size = '[{}]'.format(image_size)
			if size.lower() == 'oc':
				title = re.sub(r'([\[\(\{]([Oo][Cc])[]})])','',str(self.title))
				size = str(title)[re.search('\[',str(title)).span()[1]:re.search('\]',str(title)).span()[0]]
				size = str(' '.join(re.findall('\d+(?:\.\d+)?', size)))
				image_size = str(' '.join(re.findall('\d+(?:\.\d+)?',str(self.__image__()))))
			elif size == '':
				raise Exception('Could not get size')
			size = size.replace(' ','x')
			size = '[{}]'.format(size)
			print("{}|{}".format(size, image_size))
			if size == self.__image__():
				return True
			else:
				return False
		except Exception as e:
			print(e); pass

	def report_image(self):
		title_check = self.check_title()
		try:
			if title_check == False and self.check_database() is True:
				print('Flairing submission')
				self.submit_to_database()
				reddit.subreddit(str(self.subreddit)).flair.set(self.submission, text=self.__image__(), css_class = 'Resolution')
				self.submit_to_database()
			elif title_check == False:
				print('Discrepency has already been reported')
			else:
				print('Passing')
		except Exception as e:
			print(e)

	def run(self):
		self.report_image()

class Flair(object):

	def __init__(self, submission, subreddit):
		self.submission = submission
		self.author = submission.author
		self.subreddit = subreddit
		self.check_sticky()
		self.set_flair()

	def get_author(self):
		count = 0
		print('Checking /u/{}'.format(self.author))
		try:
			for post in reddit.subreddit(self.subreddit).search(str(self.author), limit=None):
				if self.subreddit in ['EarthPorn','QuotesPorn']:
						if str(post.subreddit) == self.subreddit and re.search(r'([\[\(\{]([Oo][Cc])[\]\}\)])',str(post.title)) and post.author == self.author and post.approved_by is not None:
							count += 1
				elif self.subreddit == 'MilitaryPorn':
						if str(post.subreddit) == self.subreddit and post.author == self.author:
							count+=1
			return(count)
		except Exception as e:
			print(e)

	def __flair__(self):
		count = self.get_author()
		flair = ''
		if self.subreddit in ['QuotesPorn','EarthPorn']:
			if count in range(1,6):
				class_ = 'Camera'
			elif count in range(6,11):
				class_ = 'Bronze'
			elif count in range(11, 21):
				class_ = 'Silver'
			elif count > 20:
				class_ = 'Gold'
			elif count == 0:
				raise Exception("Nothing")
			else:
				class_ =  None
			flair=''
		elif self.subreddit == 'MilitaryPorn':
			if count in range(10,15):
				class_ = 'private'
			elif count in range(15,25):
				class_ = 'PrivateFirstClass'
			elif count in range(25,40):
				class_ = 'Specialist'
			elif count in range(40, 50):
				class_ = 'Corporal'
			elif count in range(50,60):
				class_ = 'Sergeant'
			elif count in range(60,70):
				class_ = 'StaffSergeant'
			elif count in range(70, 80):
				class_ = 'SergeantFirstClass'
			elif count in range(80, 90):
				class_ = 'MasterSergeant'
			elif count in range(90,100):
				class_ = '2ndLT'
			elif count in range(100,120):
				class_ = '1stLt'
			elif count in range(120,140):
				class_ = 'Captain'
			elif count in range(140,160):
				class_ = 'Major'
			elif count in range(160,180):
				class_ = 'LTColonel'
			elif count in range(180,200):
				class_ = 'Colonel'
			elif count in range(200,250):
				class_ = 'BrigadierGeneral'
			elif count in range(250,500):
				class_ = 'MajorGeneral'
			elif count in range(500,750):
				class_ = 'LTGeneral'
			elif count in range(750,1000):
				class_ = 'General'
			elif count >= 1000:
				class_ = 'MilitaryPornGeneral'
			else:
				print('User does not have enough OC to warrant a flair')
				class_ = None
			flair=''
		else:
			class_ = None
		print(count, flair,class_, self.author)
		return(flair,class_)

	def check_sticky(self):
		if self.submission.stickied is True:
			raise Exception("Ignoring stickied submissions")

	def set_flair(self):
		try:
			if str(self.subreddit) == 'MilitaryPorn':
				if str(self.submission.author_flair_css_class) == self.__flair__()[1] or self.__flair__()[1] == None:
					print('Passing due to no change in flair')
					raise Exception('No change in flair')
				if str(self.submission.author_flair_css_class) not in flairs and str(self.submission.author_flair_css_class) != '':
					print('Skipping special flair')
					reddit.subreddit(str(self.subreddit)).flair.set(redditor=str(self.author),text=self.__flair__()[0], css_class = self.__flair__()[1])
					print('Flairing /u/{}'.format(self.author))
				else:
					reddit.subreddit(str(self.subreddit)).flair.set(redditor=str(self.author),text=self.__flair__()[0], css_class = self.__flair__()[1])
					print('Flairing /u/{}'.format(self.author))
			else:
				if str(self.submission.author_flair_css_class) == self.__flair__()[1]:
					print("Passing flairing user")
					pass
				else:
					reddit.subreddit(str(self.subreddit)).flair.set(redditor=str(self.author),text=self.__flair__()[0], css_class = self.__flair__()[1])
					print('Flairing /u/{}'.format(self.author))
		except:
			pass


class isRepost(object):

    def __init__(self, submission, subreddit):
        self.submission = submission
        self.subreddit = subreddit
        self.title = submission.title
        self.author = submission.author
        self.id = submission.id
        self.__repost__()
        #self.reply_to_modmail()


    def check_database(self):
    	with open('reposts.txt','r') as f:
    		if str(self.id) in f.read().split(' '):
    			return True
    		else:
    			return False

    def submit_to_database(self):
    	with open('reposts.txt','a') as f:
    		f.write(self.id + ' ')
    		f.close()

    def __repost__(self):
    	queried = reddit.subreddit(self.subreddit).search(self.title, syntax='lucene')
    	for post in queried:
    		original = '{} in {}'.format(post.title, post.subreddit)
    		current = '{} in {}'.format(self.title, self.subreddit)
    		if current == original and self.id != post.id and self.submission.created_utc > post.created_utc and self.check_database() is False and post.author != self.submission.author:
    			print('Found a repost')
    			pre = 'I have detected a possible repost by /u/{}\n\nHere is the information regarding both posts\n\n'.format(self.author)
    			table = 'Title | Author | Created | Image | Score\n-----|---------|----------|---------|------\n'
    			information = '[{}]({}) | /u/{} | {} | {} | {}\n'.format(self.title, self.submission.permalink, self.author,time.strftime('%B %e, %Y, at %T',time.localtime(self.submission.created_utc)), self.submission.url, self.submission.score)
    			information2 = '[{}]({}) | /u/{} | {} | {} | {}\n'.format(post.title, post.permalink,post.author,time.strftime('%B %e, %Y, at %T',time.localtime(post.created_utc)), post.url, post.score)
    			appendix = '\n\n---\n\nKEYS (WARNING: NOT YET FUNCTIONAL DUE TO NEW MODMAIL): !remove = !remove | !approve = approve | !report = report account farmer to admins'
    			response = pre+table+information+information2+appendix
    			reddit.subreddit(self.subreddit).message('[Notification] Repost Found',response)
    			print('Messaged successfully!')
    			self.submit_to_database()
    		else:
    			pass

    def reply_to_modmail(self):
    	for message in reddit.subreddit(self.subreddit).mod.inbox(limit=1):
    		print(message.subject)
    		if message.subject == '[Notification] Repost Found':
    			permalink = 'https://www.reddit.com' + message.body[re.search('\(').span()[1]:re.search('\)').span()[0]]
    			print(permalinks)
    			submission = reddit.submission(url=permalink)
    			for reply in message.replies:
    				if reply.body == '!remove' and submission.removed != True:
    					submission.mod.remove()
    					print('Removed')
    					reply.reply('Submission successfully removed!\n\n*This action was sponsored by your friendly Skynet overlords*')
    				elif reply.body == '!approve' and submission.approved_by is None:
    					submission.mod.approve()
    					print("Approved")
    					reply.reply('Submission successfully approved!\n\n*This action was sponsored by your friendly Skynet overlords*')
    				elif reply.body == '!report' and submission.removed is False:
    					submission.mod.remove()
    					#reddit.subreddit('reddit.com').message('Hello, I am speaking on behalf of /u/{} from /r/{}\n\nWe have reason to believe that /u/{} is a karma farmer or a spam bot (like me but not as nice). '.format(reply.author, self.subreddit, submission.author))
    					print("Messaged")
    					reply.reply("Submission successfully removed and admins ~~trolled~~ notified\n\n*This action was sponsored by your friendly Skynet overlords.*")


def image_thread(sub):
	while True:
		for submission in _reddit_.subreddit(sub).new(limit=100):
			print('[{}]'.format(threading.activeCount()))
			Image(submission, sub)

def flair_thread(sub):
	mods = ['soupyhands','t0asti','jaraxo','jaxspider','kjoneslol','thelegitmidget','pornoverlord','theredditpope','dakta','dominicdom','greatyellowshark','agentlame','kreius','elderthedog','pursuitoffappyness','milleniumfalc0n','sfitznot','i_am_still_a_idiot','gaget','scyice','dathitcha','cupcake1713','stengebt','automoderator','unknown_name','randoh12','manwithoutmodem','powerlanguagetest','jsmooth7','tehannon','kresley','ineverquitewas']
	while True:
		for submission in _reddit_.subreddit(sub).new(limit=100):
			print('[{}]'.format(threading.activeCount()))
			if str(submission.author) in ['mojave955','Music_King','phanturnedon13'] or str(submission.author).lower() in mods:
				pass
			else:
				Flair(submission, sub)

def repost_thread(sub):
	while True:
		for submission in reddit.subreddit(sub).new(limit=25):
			try:
				print('[{}]'.format(threading.activeCount()))
				isRepost(submission, sub)
			except Exception as e:
				print('Error in repost thread:',str(e))

def clear_database():
	with open('database.txt', 'r+') as f:
		if len(f.read()) > 10000:
			f.write('')
			f.close()
			print('Cleared files')
	time.sleep(60*10)

def main():
	for subreddit in multi:
		#threading.Thread(target=oc_thread, kwargs={'sub': subreddit}).start()
		threading.Thread(target=image_thread, kwargs={'sub':subreddit}).start()
		threading.Thread(target=repost_thread, kwargs={'sub':subreddit}).start()
		threading.Thread(target=flair_thread, kwargs={'sub':subreddit}).start()
		time.sleep(3)
	threading.Thread(target=clear_database).start()
	print('There are ' + str(threading.activeCount()) + ' active threads')


if __name__ == '__main__':
	main()
