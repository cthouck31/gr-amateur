import os
import logging

FILE_LOGGER_PATH   = os.path.join(os.path.expanduser("~"),
				  os.path.basename(os.path.dirname(__file__)))
FILE_LOGGER_FORMAT = "%(asctime)s [%(name)-12s][%(levelname)-8s] : %(message)s"
CONSOLE_LOGGER_FORMAT = "%(asctime)s [%(name)-12s][%(levelname)-8s] : %(message)s"


def setupLogging(level=logging.INFO, path=FILE_LOGGER_PATH, disable=[]):
	"""
	Setup logging configuration.

	Args:
		level:	Log level to set (from 'logging').
		path:	Path to output log file ('None' for no file log).

	Returns:
		Root logger object.
	"""
	# Base logger.
	rootLogger = logging.getLogger(__name__)
	# Set level.
	rootLogger.setLevel(level)

	# Create file logger.
	if path != None:
		fileHandler = logging.FileHandler(path)
		fileFmt	= logging.Formatter(FILE_LOGGER_FORMAT)
		fileHandler.setFormatter(fileFmt)
		rootLogger.addHandler(fileHandler)

	# Create console logger.
	stdHandler = logging.StreamHandler()
	stdFmt = logging.Formatter(CONSOLE_LOGGER_FORMAT)
	stdHandler.setFormatter(stdFmt)
	rootLogger.addHandler(stdHandler)

	# Set 'disabled' logger levels to ERROR to prevent
	# printing lower priority levels.
	for pkg in disable:
		tmpLogger = logging.getLogger(pkg)
		tmpLogger.setLevel(logging.ERROR)
		

	return rootLogger
