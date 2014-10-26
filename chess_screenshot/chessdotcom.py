import mechanize
import cookielib
import urllib

LOGIN_URL = 'http://www.chess.com/login'
BOARD_EDITOR_URL = 'http://www.chess.com/analysis-board-editor'
GET_NEW_DIAGRAM_ID_URL = "http://www.chess.com/api/get_diagram?id=new"
POST_DIAGRAM_URL = 'http://www.chess.com/api/get_diagram'


class PgnUploader(object):

    def __init__(self):
        self.browser = create_browser()
       
    def login(self):
        self.browser.open(LOGIN_URL)
        self.browser.select_form(nr = 0)
        self.browser.form['c1'] = 'pilipolio'
        self.browser.form['loginpassword'] = 'mallin50CC'

        # triggers some js adding other controls to the form before submitting
        # so self.browser.form.click('btnLogin') does nothing
        """ qc.pB('LoginForm', 'btnLogin', 'QClickEvent', '')
         pB => postBack: function(strForm, strControl, strEvent, strParameter)
        postBack: function(strForm, strControl, strEvent, strParameter) {
            var strForm = $j("#Qform__FormId").attr("value");
            var objForm = $j('#' + strForm);

            $j('#Qform__FormControl').attr("value", strControl);
            $j('#Qform__FormEvent').attr("value", strEvent);
            $j('#Qform__FormParameter').attr("value", strParameter);
            $j('#Qform__FormCallType').attr("value", "Server");
            $j('#Qform__FormUpdates').attr("value", this.formUpdates());
            $j('#Qform__FormCheckableControls').attr("value", this.formCheckableControls(strForm, "Server"));

            // have $j trigger the submit event (so it can catch all submit events)
            objForm.trigger("submit");
        }
        """

        addition_inputs = {
            'Qform__FormControl': 'btnLogin',
            'Qform__FormEvent': 'QClickEvent',
            #'Qform__FormParameter': '',
            'Qform__FormCallType': 'Server',
            #'Qform__FormUpdates': '',
            'Qform__FormCheckableControls': 'rememberme',
            #'Qform__FormState': '0dec296d10463d0733295bba03be1e19'
            #'Qform__FormId': 'LoginForm'
            }

        # the request need to have the js added data
        login_request = self.browser.form.click('btnLogin')    
        login_request.add_data(login_request.get_data() + '&' + to_data(addition_inputs))

        login_submit_response = self.browser.open(login_request)
        return login_submit_response.get_data()

    def upload(self, pgn_text):
        board_editor_response = self.browser.open(BOARD_EDITOR_URL)

        new_diagram_id = int(self.browser.open(GET_NEW_DIAGRAM_ID_URL).get_data())

        print "new_diagram_id = {}".format(new_diagram_id)

        #--data "id=2256802&text_setup=%26-diagramtype%3A%0AchessGame%0A%26-colorscheme%3A%0Ablue%0A%26-piecestyle%3A%0Aclassic%0A%26-float%3A%0Aleft%0A%26-flip%3A%0Afalse%0A%26-prompt%3A%0Afalse%0A%26-coords%3A%0Afalse%0A%26-size%3A%0A45%0A%26-lastmove%3A%0A%0A%26-focusnode%3A%0A%0A%26-beginnode%3A%0A%0A%26-endnode%3A%0A%0A%26-hideglobalbuttons%3A%0Afalse%0A%26-pgnbody%3A%0A%5BEvent%20%22Live%20Chess%22%5D%0A%5BSite%20%22Chess.com%22%5D%0A%5BDate%20%222014.10.18%22%5D%0A%5BWhite%20%22pilipolio%22%5D%0A%5BBlack%20%22vpmishra2003%22%5D%0A%5BResult%20%220-1%22%5D%0A%5BWhiteElo%20%22987%22%5D%0A%5BBlackElo%20%22979%22%5D%0A%5BTimeControl%20%225%7C2%22%5D%0A%5BTermination%20%22vpmishra2003%20won%20on%20time%22%5D%0A%0A1.d4%20d5%202.c4%20dxc4%203.e4%20e6%204.Bxc4%20h6%205.Nf3%20Nf6%206.Nc3%20Bd7%207.O-O%20Nc6%208.Bf4%20Bb4%209.Re1%20Bxc3%2010.bxc3%20Nh5%2011.Be3%20Qe7%2012.d5%20exd5%2013.Bxd5%20O-O-O%2014.Qb3%20Nf6%2015.Rab1%20b6%2016.Nd4%20Nxd5%2017.exd5%20Nxd4%2018.Bxd4%20Qg5%2019.a4%20Bf5%2020.Rb2%20Rhe8%2021.Rbe2%20Rxe2%2022.Rxe2%20Qc1%2B%20%0A0-1"
        #id=2257116&text_setup=%26-lastmove%3A%26-beginnode%3A%26-float%3Aleft%26-size%3A45%26-endnode%3A%26-coords%3Afalse%26-hideglobalbuttons%3Afalse%26-focusnode%3A%26-colorscheme%3Ablue%26-pgnbody%3A1.d4%2520d5%26-prompt%3Afalse%26-diagramtype%3AchessGame%26-flip%3Afalse%26-piecestyle%3Aclassic'

        post_diagram_data = to_data({
            'id': new_diagram_id,
            'text_setup': urllib.quote('&' + to_data({
                '-diagramtype': '\nchessGame\n',
                '-colorscheme': '\nblue\n',
                '-piecestyle': '\nclassic\n',
                '-float': '\nleft\n',
                '-flip': '\nfalse\n',
                '-prompt': '\nfalse\n',
                '-coords': '\nfalse\n',
                '-size': '\n45\n',
                '-lastmove': '\n\n',
                '-focusnode': '\n\n',
                '-beginnode': '\n\n',
                '-endnode': '\n\n',
                '-hideglobalbuttons': '\nfalse\n',
                '-pgnbody': '\n' + pgn_text}, equal=':'))
                })
    
        request = mechanize.Request(POST_DIAGRAM_URL)
        request.method = 'POST'
        request.add_data(post_diagram_data)
        post_diagram_response = self.browser.open(request)
        return 'http://www.chess.com/emboard?id={}'.format(new_diagram_id)


def create_browser():
    browser = mechanize.Browser()
    # fixes HTTP Error 403: request disallowed by robots.txt?
    browser.set_handle_robots(False)

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    browser.set_cookiejar(cj)

    # Browser options
    browser.set_handle_equiv(True)
    browser.set_handle_gzip(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    browser.set_debug_http(True)
    browser.set_debug_redirects(True)
    browser.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0'),
    ('X-Requested-With', 'XMLHttpRequest')]
    
    return browser


def to_data(params, equal='=', sep='&'):
            return sep.join("{}{}{}".format(k,equal, v) for k, v in params.items())
