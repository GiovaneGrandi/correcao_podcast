from config import *

chat_bp = Blueprint("chat", __name__, template_folder="templates")


@chat_bp.route("/", methods=['GET', 'POST'])
def index():
    return render_template("chat.html")