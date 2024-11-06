# Cam service
class Camera_Service_Settings:
    root_url = '127.0.0.1'
    root_port_int = 8001
    root_full_path = 'http://' + root_url + ':' + str(root_port_int)
    list_cameras = '/cameras'
    image = list_cameras + '/image/'
    image_raw = list_cameras + '/image_raw/'
    refresh = list_cameras + '/refresh'

