# translatable messages for Tina4python
import gettext

_ = gettext.gettext

MSG_DEBUG = _('Debug: {message}')
MSG_WARNING = _('Warning: {message}')
MSG_ERROR = _('Error: {message}')
MSG_INFO = _('Info: {message}')

# Router messages
MSG_ROUTER_MATCHING = _('Matching: {matching}')
MSG_ROUTER_VARIABLES = _('Variables: {variables}')
MSG_ROUTER_ROOT_PATH = _('Root Path {root_path} {url}')
MSG_ROUTER_STATIC_FILE = _('Attempting to serve static file: {static_file}')
MSG_ROUTER_CSS_FILE = _('Attempting to serve CSS file: {css_file}')
MSG_ROUTER_IMAGE_FILE = _('Attempting to serve image file: {image_file}')

# Server messages
MSG_ASSUMING_ROOT_PATH = _('Assuming root path: {root_path}, library path: {library_path}')
MSG_LOAD_ALL_THINGS = _('Load all things')
MSG_SERVER_STARTED = _('Server started http://{host_name}:{port}')
MSG_SERVER_STOPPED = _('Server stopped.')
MSG_STARTING_WEBSERVER = _('Starting webserver on {port}')
MSG_ENTRY_POINT_NAME = _('Entry point name ... {name}')

