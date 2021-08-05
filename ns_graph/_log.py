import logging
import os

LOG_PATH = os.path.join(os.getcwd(), 'log.txt')

logging.basicConfig(level=logging.INFO,
                    filename=LOG_PATH,
                    filemode='a',
                    format='%(asctime)s - %(levelname)-8s : %(funcName)s : %(message)s')

### print loggings
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
