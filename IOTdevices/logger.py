import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    fmt='%(log_color)s %(asctime)s : %(message)s',
    datefmt='%m-%d %H:%M:%S'
))

logger = colorlog.getLogger('example')
logger.setLevel('DEBUG')
logger.addHandler(handler)
