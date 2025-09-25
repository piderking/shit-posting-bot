class DownloadException(Exception):
    def __init__(self, message):
        super(message, self).__init__(message)
class UploadException(Exception):
    def __init__(self, message):
        super(message, self).__init__(message)
        
             
        

class VideoFileNotFound(Exception):
    def __init__(self, message):
        super(message, self).__init__(message)

class AudioFileNotFound(Exception):
    def __init__(self, message):
        super(message, self).__init__(message)