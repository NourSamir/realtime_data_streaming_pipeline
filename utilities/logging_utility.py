import logging

# Create and configure logger
# logging.basicConfig(filename="newfile.log",
#                     format='%(asctime)s %(message)s',
#                     filemode='w')

# Config logger
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
# logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Creating an object
logger = logging.getLogger()

# Setting the logger to DEBUG
logger.setLevel(logging.INFO)
